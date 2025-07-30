import re
import sqlparse
import inspect
from enum import Enum

from collections import defaultdict

from alembic.autogenerate.api import AutogenContext
from alembic.operations import Operations, MigrateOperation
from alembic.autogenerate import comparators, renderers
from alembic.operations.ops import UpgradeOps
from sqlalchemy import text
import sqlalchemy as sa

from core.database import registry
from core.orm.view import TableView

# ############
# View Model #
# ############

@comparators.dispatch_for("schema")
def compare_view(autogen_context: AutogenContext, upgrade_ops: UpgradeOps, schemas) -> None:
    # Define all views from the database
    db_views = defaultdict()

    for sch in schemas:
        rows = autogen_context.connection.execute(
            text(
                "SELECT table_schema, table_name, view_definition "
                "FROM information_schema.views "
                "WHERE table_schema=:nspname"
            ),
            {
                "nspname": autogen_context.dialect.default_schema_name if sch is None else sch,
            }
        )

        for row in rows:
            db_views[(row[0], row[1])] = normalize_sql(row[2])

    # Define all views from the models
    model_views = defaultdict()

    for model in registry.models.values():
        if isinstance(model.table, TableView):
            for sch in schemas:
                schema = autogen_context.dialect.default_schema_name if sch is None else sch
                definition = normalize_sql(str(model.table.selectable.compile(
                    dialect=autogen_context.dialect,
                    compile_kwargs={"literal_binds": True}
                )))
                model_views[(schema, model.meta.tablename)] = definition

    # Create new views
    for key, model_def in model_views.items():
        if key not in db_views:
            schema, name = key
            upgrade_ops.ops.append(CreateViewOperation(name, model_def))

    # Drop old views
    for key, db_def in db_views.items():
        if key not in model_views:
            schema, name = key
            upgrade_ops.ops.append(DropViewOperation(name, db_def))

    # Replace views
    for key in model_views.keys() & db_views.keys():
        model_def = model_views[key]
        model_def_for_db = normalize_sql(model_def, True)
        db_def = db_views[key]

        if model_def_for_db != db_def:
            schema, name = key
            upgrade_ops.ops.append(ReplaceViewOperation(name, model_def, db_def))


@Operations.register_operation("create_view")
class CreateViewOperation(MigrateOperation):
    def __init__(self, name: str, definition: str) -> None:
        self.name: str = name
        self.definition: str = definition

    @classmethod
    def create_view(cls, operations, name: str, definition: str) -> None:
        return operations.invoke(cls(name, definition))

    def reverse(self) -> MigrateOperation:
        return DropViewOperation(self.name, self.definition)


@Operations.register_operation("drop_view")
class DropViewOperation(MigrateOperation):
    def __init__(self, name: str, reverse_definition: str) -> None:
        self.name: str = name
        self.reverse_definition: str = reverse_definition

    @classmethod
    def drop_view(cls, operations, name: str, reverse_definition: str) -> None:
        return operations.invoke(cls(name, reverse_definition))

    def reverse(self) -> MigrateOperation:
        return CreateViewOperation(self.name, self.reverse_definition)


@Operations.register_operation("replace_view")
class ReplaceViewOperation(MigrateOperation):
    def __init__(self, name: str, definition: str, reverse_definition: str | None) -> None:
        self.name: str = name
        self.definition: str = definition
        self.reverse_definition: str | None = reverse_definition

    @classmethod
    def replace_view(cls, operations, name: str, definition: str, reverse_definition: str) -> None:
        operations.invoke(cls(name, definition, reverse_definition))

    def reverse(self) -> MigrateOperation:
        return ReplaceViewOperation(self.name, self.reverse_definition, self.definition)


@Operations.implementation_for(CreateViewOperation)
def create_view(operations, operation: CreateViewOperation) -> None:
    operations.execute(f"CREATE VIEW {operation.name} AS {operation.definition}")


@Operations.implementation_for(DropViewOperation)
def drop_view(operations, operation: DropViewOperation) -> None:
    operations.execute(f"DROP VIEW IF EXISTS {operation.name} CASCADE")


@Operations.implementation_for(ReplaceViewOperation)
def replace_view(operations, operation: ReplaceViewOperation) -> None:
    operations.execute(f"DROP VIEW IF EXISTS {operation.name} CASCADE")
    operations.execute(f"CREATE OR REPLACE VIEW {operation.name} AS {operation.definition}")


@renderers.dispatch_for(CreateViewOperation)
def render_create_view(_, operation: CreateViewOperation) -> str:
    return f"op.create_view('{operation.name}', '''{operation.definition}''')"


@renderers.dispatch_for(DropViewOperation)
def render_drop_view(_, operation: DropViewOperation) -> str:
    return f"op.drop_view('{operation.name}', '''{operation.reverse_definition}''')"


@renderers.dispatch_for(ReplaceViewOperation)
def render_replace_view(_, operation: ReplaceViewOperation) -> str:
    return f"op.replace_view('{operation.name}', '''{operation.definition}''', '''{operation.reverse_definition}''')"


def normalize_sql(sql: str, clean_null_cast: bool = False) -> str:
    formatted = sqlparse.format(
        sql,
        keyword_case='lower',
        identifier_case='lower',
        strip_comments=True,
        reindent=False,
        use_space_around_operators=True,
    )

    formatted = re.sub(r"(::)\s*[a-zA-Z0-9_.\s]+?(\s+varying)?(?=\s+as\s+|\s*,|\s*\)|\s*$)", "", formatted)
    formatted = re.sub(r"varchar(\([0-9]+\))?", "", formatted, flags=re.IGNORECASE)
    formatted = re.sub(r"character varying(\([0-9]+\))?", "", formatted, flags=re.IGNORECASE)
    formatted = re.sub(r"\s+", " ", formatted)
    formatted = re.sub(r"\(\s*", "(", formatted)
    formatted = re.sub(r"\s*\)", ")", formatted)
    formatted = re.sub(r'([a-zA-Z0-9_."()]+)\s+as\s+("[a-zA-Z0-9_]+"|[a-zA-Z0-9_]+)', _remove_redundant_aliases, formatted, flags=re.IGNORECASE)

    if clean_null_cast:
        formatted = re.sub(r'cast\s*\(\s*null\s+as\s+[^)]+\)', 'null', sql, flags=re.IGNORECASE)

    formatted = formatted.strip()
    formatted = formatted.strip(";")

    return formatted


def _remove_redundant_aliases(match):
    expr = match.group(1).strip()
    alias = match.group(2).strip().strip('"')
    expr_last = expr.split('.')[-1].strip('"')

    if expr_last == alias:
        return expr

    return match.group(0)


# #######
# Enums #
# #######

@comparators.dispatch_for("schema")
def compare_enums(autogen_context: AutogenContext, upgrade_ops: UpgradeOps, schemas) -> None:
    # Get all enums from the database
    db_enums = {}

    for sch in schemas:
        rows = autogen_context.connection.execute(
            text(
                "SELECT t.typname, e.enumlabel "
                "FROM pg_type t "
                "JOIN pg_enum e ON t.oid = e.enumtypid "
                "JOIN pg_namespace n ON t.typnamespace = n.oid "
                "WHERE n.nspname=:nspname "
                "ORDER BY t.typname, e.enumsortorder"
            ),
            {
                "nspname": autogen_context.dialect.default_schema_name if sch is None else sch,
            }
        )

        for row in rows:
            enum_name, enum_value = row
            if enum_name not in db_enums:
                db_enums[enum_name] = []
            db_enums[enum_name].append(enum_value)

    # Get all enums from models
    model_enums = {}

    for model in registry.models.values():
        for field_name, field in model.meta.fields.items():
            # Check for ChoiceField with enum
            choices = getattr(field, 'choices', None)
            if choices and inspect.isclass(choices) and issubclass(choices, Enum):
                enum_class = choices
                enum_name = enum_class.__name__.lower()

                # Convert to the actual postgres enum name format
                if enum_name not in model_enums:
                    model_enums[enum_name] = [e.name for e in enum_class]

    # Compare and create operations
    for enum_name, model_values in model_enums.items():
        if enum_name in db_enums:
            db_values = db_enums[enum_name]
            if set(model_values) != set(db_values):
                # Enum values have changed
                upgrade_ops.ops.append(ReplaceEnumOperation(enum_name, model_values, db_values))
        else:
            # New enum
            upgrade_ops.ops.append(CreateEnumOperation(enum_name, model_values))

    # Check for dropped enums
    for enum_name, db_values in db_enums.items():
        if enum_name not in model_enums:
            upgrade_ops.ops.append(DropEnumOperation(enum_name, db_values))


@Operations.register_operation("replace_enum")
class ReplaceEnumOperation(MigrateOperation):
    def __init__(self, enum_name: str, new_values: list[str], old_values: list[str], value_mapping: dict[str, str] | None = None) -> None:
        self.enum_name: str = enum_name
        self.new_values: list[str] = new_values
        self.old_values: list[str] = old_values
        self.value_mapping: dict[str, str] | None = value_mapping

    @classmethod
    def replace_enum(cls, operations, enum_name: str, new_values: list[str], old_values: list[str], value_mapping: dict[str, str] | None = None) -> None:
        return operations.invoke(cls(enum_name, new_values, old_values, value_mapping))

    def reverse(self) -> MigrateOperation:
        reverse_mapping = None
        if self.value_mapping:
            reverse_mapping = {v: k for k, v in self.value_mapping.items()}
        return ReplaceEnumOperation(self.enum_name, self.old_values, self.new_values, reverse_mapping)


@Operations.register_operation("create_enum")
class CreateEnumOperation(MigrateOperation):
    def __init__(self, enum_name: str, values: list[str]) -> None:
        self.enum_name: str = enum_name
        self.values: list[str] = values

    @classmethod
    def create_enum(cls, operations, enum_name: str, values: list[str]) -> None:
        return operations.invoke(cls(enum_name, values))

    def reverse(self) -> MigrateOperation:
        return DropEnumOperation(self.enum_name, self.values)


@Operations.register_operation("drop_enum")
class DropEnumOperation(MigrateOperation):
    def __init__(self, enum_name: str, reverse_values: list[str]) -> None:
        self.enum_name: str = enum_name
        self.reverse_values: list[str] = reverse_values

    @classmethod
    def drop_enum(cls, operations, enum_name: str, reverse_values: list[str]) -> None:
        return operations.invoke(cls(enum_name, reverse_values))

    def reverse(self) -> MigrateOperation:
        return CreateEnumOperation(self.enum_name, self.reverse_values)


@Operations.implementation_for(ReplaceEnumOperation)
def replace_enum(operations, operation: ReplaceEnumOperation) -> None:
    enum_name = operation.enum_name
    old_enum_name = f"{enum_name}_old"
    new_values = operation.new_values

    # Rename old enum
    operations.execute(f"ALTER TYPE {enum_name} RENAME TO {old_enum_name}")

    # Create new enum with new values
    values_str = "', '".join(new_values)
    new_enum = sa.Enum(*new_values, name=enum_name)
    new_enum.create(operations.get_bind())

    # Find all tables using this enum and update them
    result = operations.get_bind().execute(sa.text(
        "SELECT table_name, column_name, is_nullable FROM information_schema.columns WHERE udt_name = :old_enum_name"
    ), {"old_enum_name": old_enum_name})

    for row in result:
        table_name, column_name, is_nullable = row
        default_value = f"'{new_values[0]}'" if new_values else "null"

        # Build CASE statement for value conversion
        if operation.value_mapping:
            # Use custom mapping provided by user
            case_conditions = []
            for old_val, new_val in operation.value_mapping.items():
                case_conditions.append(f"WHEN {column_name}::text = '{old_val}' THEN '{new_val}'::{enum_name}")

            # Add case-insensitive fallback for unmapped values
            case_insensitive_conditions = []
            for new_val in new_values:
                case_insensitive_conditions.append(f"WHEN LOWER({column_name}::text) = LOWER('{new_val}') THEN '{new_val}'::{enum_name}")

            # Final fallback
            if is_nullable == "YES":
                final_fallback = "null"
            else:
                final_fallback = f"{default_value}::{enum_name}"

            case_statement = f"""CASE 
                {' '.join(case_conditions)}
                {' '.join(case_insensitive_conditions)}
                ELSE {final_fallback}
            END"""
        else:
            # Use automatic mapping (existing values that match new enum values)
            # First try exact match, then case-insensitive match
            case_insensitive_conditions = []
            for new_val in new_values:
                case_insensitive_conditions.append(f"WHEN LOWER({column_name}::text) = LOWER('{new_val}') THEN '{new_val}'::{enum_name}")

            if is_nullable == "YES":
                case_statement = f"""CASE 
                    WHEN {column_name}::text = ANY(ARRAY{new_values}) THEN {column_name}::text::{enum_name}
                    {' '.join(case_insensitive_conditions)}
                    ELSE null
                END"""
            else:
                case_statement = f"""CASE 
                    WHEN {column_name}::text = ANY(ARRAY{new_values}) THEN {column_name}::text::{enum_name}
                    {' '.join(case_insensitive_conditions)}
                    ELSE {default_value}::{enum_name}
                END"""

        operations.execute(f"""
            ALTER TABLE {table_name}
            ALTER COLUMN {column_name}
            TYPE {enum_name}
            USING {case_statement}
        """)

    # Drop old enum
    sa.Enum(name=old_enum_name).drop(operations.get_bind(), checkfirst=True)


@Operations.implementation_for(CreateEnumOperation)
def create_enum(operations, operation: CreateEnumOperation) -> None:
    result = operations.get_bind().execute(sa.text("SELECT 1 FROM pg_type WHERE typname = :enum_name"), {"enum_name": operation.enum_name}).fetchone()

    if result:
        return

    enum = sa.Enum(*operation.values, name=operation.enum_name)
    enum.create(operations.get_bind())


@Operations.implementation_for(DropEnumOperation)
def drop_enum(operations, operation: DropEnumOperation) -> None:
    sa.Enum(name=operation.enum_name).drop(operations.get_bind(), checkfirst=True)


@renderers.dispatch_for(ReplaceEnumOperation)
def render_replace_enum(_, operation: ReplaceEnumOperation) -> str:
    new_values_repr = repr(operation.new_values)
    old_values_repr = repr(operation.old_values)
    if operation.value_mapping:
        value_mapping_repr = repr(operation.value_mapping)
        return f"op.replace_enum('{operation.enum_name}', {new_values_repr}, {old_values_repr}, {value_mapping_repr})"
    else:
        return f"op.replace_enum('{operation.enum_name}', {new_values_repr}, {old_values_repr})"


@renderers.dispatch_for(CreateEnumOperation)
def render_create_enum(_, operation: CreateEnumOperation) -> str:
    values_repr = repr(operation.values)
    return f"op.create_enum('{operation.enum_name}', {values_repr})"


@renderers.dispatch_for(DropEnumOperation)
def render_drop_enum(_, operation: DropEnumOperation) -> str:
    reverse_values_repr = repr(operation.reverse_values)
    return f"op.drop_enum('{operation.enum_name}', {reverse_values_repr})"
