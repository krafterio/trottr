from typing import Any

import sqlalchemy as sa
from inspect import isclass

from edgy import ForeignKey, ManyToMany, Model
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.orm.attributes import InstrumentedAttribute
from pydantic import BaseModel as PydanticBaseModel

def extract_field_names(record: dict, parent_field: str = '') -> list[str]:
    fields = []

    for record_field, record_val in record.items():
        record_field_name = f"{parent_field}.{record_field}" if parent_field else record_field

        if isinstance(record_val, dict):
            fields.extend(extract_field_names(record_val, record_field_name))
        else:
            fields.append(record_field_name)

    return fields


def get_columns(mixed):
    """
    Return a list of all Column objects for given SQLAlchemy object.

    The type of the list depends on the type of the object to return the
    columns from.

    ::

        get_columns(User)

        get_columns(User())

        get_columns(User.__table__)

        get_columns(User.__mapper__)

        get_columns(sa.orm.aliased(User))

        get_columns(sa.orm.alised(User.__table__))


    :param mixed:
        SA Table object, SA Mapper, SA declarative class, SA declarative class
        instance or an alias of any of these objects
    """
    if isinstance(mixed, sa.sql.selectable.Selectable):
        return mixed.selected_columns
    if isinstance(mixed, sa.orm.util.AliasedClass):
        return sa.inspect(mixed).mapper.columns
    if isinstance(mixed, sa.orm.Mapper):
        return mixed.columns
    if isinstance(mixed, InstrumentedAttribute):
        return mixed.property.columns
    if isinstance(mixed, ColumnProperty):
        return mixed.columns
    if isinstance(mixed, sa.Column):
        return [mixed]
    if not isclass(mixed):
        mixed = mixed.__class__
    return sa.inspect(mixed).columns


async def get_value_from_path(instance: Model, path: str) -> Any | None:
    async def _resolve(obj_or_list: Model | list[Model], path_parts: list[str] | None) -> Any | None:
        if not path_parts:
            return obj_or_list

        key = path_parts[0]
        rest = path_parts[1:]

        if isinstance(obj_or_list, list):
            results = []

            for obj in obj_or_list:
                val = await _resolve(obj, path_parts)

                if isinstance(val, list):
                    results.extend(val)
                else:
                    results.append(val)

            return results

        if not hasattr(obj_or_list, key):
            return None

        value = getattr(obj_or_list, key)
        field = obj_or_list.meta.fields.get(key, None)

        if hasattr(value, "all") and callable(value.all):
            value = await value.all()

            return await _resolve(value, rest or ['id'])

        if field and isinstance(field, (ForeignKey, ManyToMany)):
            return await _resolve(value, rest or ['id'])

        if rest:
            raise ValueError(f"Le champ '{key}' n'est pas une relation, impossible de continuer avec '{'.'.join(rest)}'")

        return value

    return await _resolve(instance, path.split('.'))


def model_validator_extra_fields(model_name: str, values, handler, extra_field_name: str = 'extra') -> Any:
    from core import context
    from pydantic_core import InitErrorDetails
    from pydantic import TypeAdapter, ValidationError

    handler_result = None
    handler_errors: list[InitErrorDetails | dict] = []
    extra_errors: list[InitErrorDetails | dict] = []
    validation_title = "ValidatorCallable"

    try:
        extra_fields = context.get_map_workspace_extra_fields(model_name)

        for name, value in values.items():
            if name.startswith(f"{extra_field_name}_"):
                extra_name = name[len(extra_field_name) + 1:]

                if extra_name in extra_fields:
                    from models.workspace_extra_field import EXTRA_FIELDS_MAP, EXTRA_FIELD_TYPE_OPTIONS

                    extra_field = extra_fields[extra_name]
                    model_field_type = EXTRA_FIELDS_MAP[extra_field.field_type]

                    ft = model_field_type(**EXTRA_FIELD_TYPE_OPTIONS[extra_field.field_type])
                    type_adapter = TypeAdapter(ft.annotation)

                    try:
                        if value is None:
                            if extra_field.required:
                                values[name] = type_adapter.validate_python(value)
                            else:
                                values[name] = None
                        else:
                            values[name] = type_adapter.validate_python(value)
                    except ValidationError as e:
                        from pydantic_core import ErrorDetails

                        for error in e.errors():
                            extra_errors.append({
                                **error,
                                "loc": (name,),
                            })
                else:
                    extra_errors.append(InitErrorDetails(
                        type='extra_forbidden',
                        loc=(name,),
                        input=value,
                    ))

        handler_result = handler(values)
    except ValidationError as ve:
        validation_title = ve.title
        handler_errors = ve.errors()

    if handler_errors or extra_errors:
        raise ValidationError.from_exception_data(
            validation_title,
            handler_errors + extra_errors,
        )

    return handler_result
