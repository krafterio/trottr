from typing import Literal, TypeAlias, Any, get_args, cast, Callable
from dataclasses import dataclass
import json

from edgy import (
    QuerySet,
    Model,
    Q,
    not_,
    IntegerField,
    BooleanField,
    CharField,
    ChoiceField,
    DateField,
    DateTimeField,
    DurationField,
    DecimalField,
    FileField,
    FloatField,
    ForeignKey,
    RefForeignKey,
    ManyToMany,
    IPAddressField,
    JSONField,
    BinaryField,
    OneToOne,
    TimeField,
    UUIDField,
)
from edgy.core.db.fields import BaseFieldType
from fastapi.params import Query, Header
from sqlalchemy import null


FilterOperator: TypeAlias = Literal[
    '=',
    '!=',
    '<',
    '<=',
    '>',
    '>=',
    'between',
    'like',
    'ilike',
    'not like',
    'not ilike',
    'starts with',
    'ends with',
    'not starts with',
    'not ends with',
    'contains',
    'icontains',
    'not contains',
    'not icontains',
    'match',
    'in',
    'not in',
    'is true',
    'is false',
    'is empty',
    'is not empty',
]


FilterConditionType: TypeAlias = Literal[
    '&',
    '|',
]


FILTER_OPERATORS_SQL = {
    '=': lambda c, v: c.__eq__(v),
    '!=': lambda c, v: c.__ne__(v),
    '<': lambda c, v: c.__lt__(v),
    '<=': lambda c, v: c.__le__(v),
    '>': lambda c, v: c.__gt__(v),
    '>=': lambda c, v: c.__ge__(v),
    'between': lambda c, v: c.between(*v),
    'like': lambda c, v: c.like(v),
    'ilike': lambda c, v: c.ilike(v),
    'not like': lambda c, v: c.notlike(v),
    'not ilike': lambda c, v: c.notilike(v),
    'starts with': lambda c, v: c.startswith(v),
    'ends with': lambda c, v: c.endswith(v),
    'not starts with': lambda c, v: not_(c.startswith(v)),
    'not ends with': lambda c, v: not_(c.endswith(v)),
    'contains': lambda c, v: c.contains(v),
    'icontains': lambda c, v: c.icontains(v),
    'not contains': lambda c, v: not_(c.contains(v)),
    'not icontains': lambda c, v: not_(c.icontains(v)),
    'match': lambda c, v: c.match(v),
    'in': lambda c, v: c.in_(v),
    'not in': lambda c, v: c.not_in(v),
    'is true': lambda c, v = None: c.is_(True),
    'is false': lambda c, v = None: c.is_(False),
    'is empty': lambda c, v = None: c.is_(null()),
    'is not empty': lambda c, v = None: c.is_not(null()),
}


FILTER_DICT_OPERATORS_SQL = {
    '=': lambda qs, f, v: Q({f"{f.replace('.', '__')}": v}),
    '!=': lambda qs, f, v: qs.not_(Q({f"{f.replace('.', '__')}": v})),
    '<': lambda qs, f, v: Q({f"{f.replace('.', '__')}__lt": v}),
    '<=': lambda qs, f, v: Q({f"{f.replace('.', '__')}__le": v}),
    '>': lambda qs, f, v: Q({f"{f.replace('.', '__')}__gt": v}),
    '>=': lambda qs, f, v: Q({f"{f.replace('.', '__')}__ge": v}),
    'between': lambda qs, f, v: Q({f"{f.replace('.', '__')}__ge": v[0], f"{f.replace('.', '__')}__le": v[1]}),
    'like': lambda qs, f, v: Q({f"{f.replace('.', '__')}__like": v}),
    'ilike': lambda qs, f, v: Q({f"{f.replace('.', '__')}__ilike": v}),
    'not like': lambda qs, f, v: qs.not_(Q({f"{f.replace('.', '__')}__like": v})),
    'not ilike': lambda qs, f, v: qs.not_(Q({f"{f.replace('.', '__')}__ilike": v})),
    'starts with': lambda qs, f, v: Q({f"{f.replace('.', '__')}__startswith": v}),
    'ends with': lambda qs, f, v: Q({f"{f.replace('.', '__')}__endswith": v}),
    'not starts with': lambda qs, f, v: qs.not_(Q({f"{f.replace('.', '__')}__startswith": v})),
    'not ends with': lambda qs, f, v: qs.not_(Q({f"{f.replace('.', '__')}__endswith": v})),
    'contains': lambda qs, f, v: Q({f"{f.replace('.', '__')}__contains": v}),
    'icontains': lambda qs, f, v: Q({f"{f.replace('.', '__')}__icontains": v}),
    'not contains': lambda qs, f, v: qs.not_(Q({f"{f.replace('.', '__')}__contains": v})),
    'not icontains': lambda qs, f, v: qs.not_(Q({f"{f.replace('.', '__')}__icontains": v})),
    'match': lambda qs, f, v: Q({f"{f.replace('.', '__')}__match": v}),
    'in': lambda qs, f, v: Q({f"{f.replace('.', '__')}__in": v}),
    'not in': lambda qs, f, v: qs.not_(Q({f"{f.replace('.', '__')}__in": v})),
    'is true': lambda qs, f, v: Q({f"{f.replace('.', '__')}__is": True}),
    'is false': lambda qs, f, v: Q({f"{f.replace('.', '__')}__is": False}),
    'is empty': lambda qs, f, v: Q({f"{f.replace('.', '__')}__is": None}),
    'is not empty': lambda qs, f, v: qs.not_(Q({f"{f.replace('.', '__')}__is": None})),
}


FILTER_OPERATORS_SQL_UNPACK = {
    'between': 2,
}


FILTER_OPERATORS_FIELD_MAP = {
    IntegerField: [
        '=',
        '!=',
        '<',
        '<=',
        '>',
        '>=',
        'between',
        'in',
        'not in',
        'is empty',
        'is not empty',
    ],
    BooleanField: [
        'is true',
        'is false',
    ],
    CharField: [
        '=',
        '!=',
        'like',
        'ilike',
        'not like',
        'not ilike',
        'starts with',
        'ends with',
        'not starts with',
        'not ends with',
        'contains',
        'icontains',
        'not contains',
        'not icontains',
        'match',
        'in',
        'not in',
        'is empty',
        'is not empty',
    ],
    ChoiceField: [
        '=',
        '!=',
        'in',
        'not in',
        'is empty',
        'is not empty',
    ],
    DateField: [
        '=',
        '!=',
        '<',
        '<=',
        '>',
        '>=',
        'between',
        'is empty',
        'is not empty',
    ],
    DateTimeField: [
        '=',
        '!=',
        '<',
        '<=',
        '>',
        '>=',
        'between',
        'is empty',
        'is not empty',
    ],
    DurationField: [
        '=',
        '!=',
        '<',
        '<=',
        '>',
        '>=',
        'between',
        'in',
        'not in',
        'is empty',
        'is not empty',
    ],
    DecimalField: [
        '=',
        '!=',
        '<',
        '<=',
        '>',
        '>=',
        'between',
        'in',
        'not in',
        'is empty',
        'is not empty',
    ],
    FileField: [
        'is empty',
        'is not empty',
    ],
    FloatField: [
        '=',
        '!=',
        '<',
        '<=',
        '>',
        '>=',
        'between',
        'in',
        'not in',
        'is empty',
        'is not empty',
    ],
    ForeignKey: [
        '=',
        '!=',
        'in',
        'not in',
        'is empty',
        'is not empty',
    ],
    RefForeignKey: [
        '=',
        '!=',
        'in',
        'not in',
        'is empty',
        'is not empty',
    ],
    ManyToMany: [
        'in',
        'not in',
        'is empty',
        'is not empty',
    ],
    IPAddressField: [
        '=',
        '!=',
        'like',
        'ilike',
        'not like',
        'not ilike',
        'starts with',
        'ends with',
        'not starts with',
        'not ends with',
        'contains',
        'icontains',
        'not contains',
        'not icontains',
        'match',
        'in',
        'not in',
        'is empty',
        'is not empty',
    ],
    JSONField: [
        'is empty',
        'is not empty',
    ],
    BinaryField: [
        'is empty',
        'is not empty',
    ],
    OneToOne: [
        '=',
        '!=',
        'in',
        'not in',
        'is empty',
        'is not empty',
    ],
    TimeField: [
        '=',
        '!=',
        '<',
        '<=',
        '>',
        '>=',
        'between',
        'in',
        'not in',
        'is empty',
        'is not empty',
    ],
    UUIDField: [
        '=',
        '!=',
        'like',
        'ilike',
        'not like',
        'not ilike',
        'starts with',
        'ends with',
        'not starts with',
        'not ends with',
        'contains',
        'icontains',
        'not contains',
        'not icontains',
        'match',
        'in',
        'not in',
        'is empty',
        'is not empty',
    ],
}


class InvalidFilterError(Exception):...


class FilterQuery(Query):
    def __init__(self):
        super().__init__(
            default=None,
            title="Filter",
            description="Filter the list of items with the filter expression build with rules and conditions",
        )


class FilterHeader(Header):
    def __init__(self):
        super().__init__(
            default=None,
            title="Filter",
            description="Filter the list of items with the filter expression build with rules and conditions",
            alias="X-Filter",
        )


@dataclass(frozen=True)
class FilterRule:
    field: str
    operator: FilterOperator
    value: Any | None = None

    def __post_init__(self):
        if self.operator not in get_args(FilterOperator):
            raise ValueError(f"Operator '{self.operator}' is not supported")


@dataclass(frozen=True)
class FilterCondition:
    condition: FilterConditionType
    rules: list[FilterRule | type("FilterCondition")]

    def __post_init__(self):
        if self.condition not in get_args(FilterConditionType):
            raise ValueError(f"Condition '{self.condition}' is not supported")


@dataclass(frozen=True)
class R(FilterRule):...


class And(FilterCondition):
    def __init__(self, *rules: FilterRule | FilterCondition):
        super().__init__(condition='&', rules=list(rules))


class Or(FilterCondition):
    def __init__(self, *rules: FilterRule | FilterCondition):
        super().__init__(condition='|', rules=list(rules))


FilterRules = list[FilterRule | FilterCondition]
Filter = FilterRule | FilterCondition | FilterRules


FilterRuleTuple = tuple[str, FilterOperator, Any | None]
FilterRulesTuple = list[FilterRuleTuple | type('FilterConditionTuple')]
FilterConditionTuple = tuple[FilterConditionType, FilterRulesTuple]
FilterTuple = FilterRuleTuple | FilterConditionTuple | FilterRulesTuple


def is_rule(item: Any) -> bool:
    if isinstance(item, FilterRule):
        return True

    return (
        (isinstance(item, tuple) or isinstance(item, list))
        and 2 <= len(item) <= 3
        and isinstance(item[0], str)
        and isinstance(item[1], str)
    )


def is_condition(item: Any) -> bool:
    if isinstance(item, FilterCondition):
        return True

    return (
        (isinstance(item, tuple) or isinstance(item, list))
        and len(item) == 2
        and isinstance(item[0], str)
        and isinstance(item[1], list)
    )


def parse_filter_input(filters: str | list | FilterTuple | None) -> FilterCondition | None:
    if isinstance(filters, str):
        return parse_filter_input_str(filters)

    if isinstance(filters, list):
        filters = parse_filter_input_array_to_tuple(filters)

    if isinstance(filters, tuple):
        return parse_filter_input_tuple(filters)

    return None


def parse_filter_input_str(filters: str | None) -> FilterCondition | None:
    if not filters:
        return None

    try:
        data = json.loads(filters)
        tuple_data = parse_filter_input_array_to_tuple(data)

        return parse_filter_input_tuple(tuple_data)
    except json.JSONDecodeError:
        raise InvalidFilterError("Invalid JSON filter expression")


def parse_filter_input_array_to_tuple(filters: list | None) -> FilterTuple | None:
    if not filters:
        return None

    if len(filters) == 0:
        return None

    # Filter Condition
    if is_condition(filters):
        parsed_rules = []

        for rule in filters[1]:
            if isinstance(rule, list):
                parsed_rule = parse_filter_input_array_to_tuple(rule)

                if parsed_rule:
                    parsed_rules.append(parsed_rule)
            else:
                parsed_rules.append(rule)

        return filters[0], parsed_rules

    # Filter Rule
    if is_rule(filters):
        if len(filters) == 2:
            return filters[0], filters[1]
        else:
            return filters[0], filters[1], filters[2]

    # Array
    parsed_items = []

    for item in filters:
        if isinstance(item, list):
            parsed_item = parse_filter_input_array_to_tuple(item)

            if parsed_item:
                parsed_items.append(parsed_item)
        else:
            parsed_items.append(item)

    if parsed_items:
        return '&', parsed_items

    raise InvalidFilterError("Invalid filter expression")


def parse_filter_input_tuple(filters: FilterTuple | None) -> FilterCondition | None:
    if not filters:
        return None

    if is_rule(filters):
        rule_tuple = cast(FilterRuleTuple, filters)
        rule = create_rule_from_tuple(rule_tuple)

        return And(rule) if rule else None

    if is_condition(filters):
        condition_tuple = cast(FilterConditionTuple, filters)

        return create_condition_from_tuple(condition_tuple)

    if isinstance(filters, list):
        items = []

        for item in filters:
            if is_rule(item):
                rule = create_rule_from_tuple(cast(FilterRuleTuple, item))

                if rule:
                    items.append(rule)
            elif is_condition(item):
                condition = create_condition_from_tuple(cast(FilterConditionTuple, item))

                if condition:
                    items.append(condition)

        if items:
            return And(*items)

    raise InvalidFilterError("Invalid filter expression")


def create_rule_from_tuple(rule_tuple: FilterRuleTuple) -> FilterRule | None:
    if len(rule_tuple) < 2:
        raise InvalidFilterError("Rule must have at least 2 elements")

    field = rule_tuple[0]
    operator = cast(FilterOperator, rule_tuple[1])

    if operator not in get_args(FilterOperator):
        raise InvalidFilterError(f"Operator '{operator}' is not supported")

    value = rule_tuple[2] if len(rule_tuple) > 2 else None

    return R(field, operator, value)


def create_condition_from_tuple(condition_tuple: FilterConditionTuple) -> FilterCondition | None:
    if len(condition_tuple) != 2:
        raise InvalidFilterError("Condition must have 2 elements")

    condition_type = cast(FilterConditionType, condition_tuple[0])
    rules_data = condition_tuple[1]

    if condition_type not in get_args(FilterConditionType):
        raise InvalidFilterError(f"Condition type '{condition_type}' is not supported")

    rules = []

    for rule_data in rules_data:
        if is_rule(rule_data):
            rule = create_rule_from_tuple(cast(FilterRuleTuple, rule_data))

            if rule:
                rules.append(rule)
        elif is_condition(rule_data):
            nested_condition = create_condition_from_tuple(cast(FilterConditionTuple, rule_data))

            if nested_condition:
                rules.append(nested_condition)

    if condition_type == '&':
        return And(*rules) if rules else None
    else:
        return Or(*rules) if rules else None


def merge_filters(*filters: Filter) -> FilterCondition | None:
    parsed_filters = []

    for filter_item in filters:
        if filter_item is None:
            continue

        if isinstance(filter_item, str):
            parsed = parse_filter_input_str(filter_item)

            if parsed:
                parsed_filters.append(parsed)
        elif isinstance(filter_item, (tuple, list)):
            parsed = parse_filter_input_tuple(filter_item) # type: ignore

            if parsed:
                parsed_filters.append(parsed)
        elif isinstance(filter_item, (FilterRule, FilterCondition)):
            parsed_filters.append(filter_item)

    if not parsed_filters:
        return None

    if len(parsed_filters) == 1:
        if isinstance(parsed_filters[0], FilterCondition):
            return parsed_filters[0]
        else:
            return And(parsed_filters[0])

    return And(*parsed_filters)


def add_prefix_on_fields(field_prefix: str, filters: list | FilterTuple | None) -> FilterTuple | None:
    if not filters:
        return None

    if isinstance(filters, list):
        filters = parse_filter_input_array_to_tuple(filters)

    if is_rule(filters):
        field, operator, value = filters

        return f"{field_prefix}.{field}", operator, value

    elif is_condition(filters):
        condition, rules = filters
        new_rules = []

        for rule in rules:
            new_rules.append(add_prefix_on_fields(field_prefix, rule))

        return condition, new_rules

    elif isinstance(filters, list):
        return [add_prefix_on_fields(field_prefix, item) for item in filters]

    return filters


def validate_filters(model_cls: type[Model], filters: Filter | None) -> FilterCondition | None:
    if not filters:
        return None

    # Filter Rule
    if is_rule(filters):
        if not validate_filter_field(model_cls, filters.field):
            raise InvalidFilterError(f'Invalid filter field: {filters.field}')

        if not validate_filter_operator(model_cls, filters.field, filters.operator):
            raise InvalidFilterError(f'Invalid operator {filters.operator} for field {filters.field}')

        return filters

    # Filter Condition
    if is_condition(filters):
        validated_rules = []

        for rule in filters.rules:
            validated_rule = validate_filters(model_cls, rule)

            if validated_rule:
                validated_rules.append(validated_rule)

        if validated_rules:
            if filters.condition == '&':
                return And(*validated_rules)
            else:
                return Or(*validated_rules)

    raise InvalidFilterError("Invalid filter expression")


def validate_filter_field(model_cls: type[Model], field_path: str) -> bool:
    if not field_path:
        return False

    if field_path.startswith('extra_'):
        pass

    parts = field_path.split('.')
    current_cls = model_cls

    for i, part in enumerate(parts):
        if part not in current_cls.meta.fields:
            return False

        field_info = current_cls.meta.fields.get(part)

        if i < len(parts) - 1:
            if hasattr(field_info, 'target'):
                current_cls = field_info.target
            else:
                return False

    return True


def validate_filter_operator(model_cls: type[Model], field_path: str, operator: str) -> bool:
    if not field_path or not operator:
        return False

    if field_path.startswith('extra_'):
        pass

    parts = field_path.split('.')
    current_cls = model_cls

    for i, part in enumerate(parts):
        if part not in current_cls.meta.fields:
            return False

        field_info = current_cls.meta.fields.get(part)

        if i < len(parts) - 1:
            if hasattr(field_info, 'target'):
                current_cls = field_info.target
            else:
                return False
        else:
            return operator in get_filter_operators(field_info)

    return False


def get_filter_operators(field_info: BaseFieldType) -> list[str]:
    field_type = type(field_info)

    if field_type in FILTER_OPERATORS_FIELD_MAP:
        return FILTER_OPERATORS_FIELD_MAP[field_type]

    for map_field_type, allowed_operators in FILTER_OPERATORS_FIELD_MAP.items():
        if isinstance(field_info, map_field_type):
            return allowed_operators

    return []


def build_filter_expression(model_cls: type[Model], filters: FilterRule | FilterCondition) -> Any | None:
    cond_query = cast(QuerySet, model_cls.global_query if hasattr(model_cls, 'global_query') else model_cls.query)

    if isinstance(filters, FilterRule):
        field = filters.field
        operator_method = FILTER_OPERATORS_SQL.get(filters.operator, None)
        operator_dict_method = FILTER_DICT_OPERATORS_SQL.get(filters.operator, None)

        if not operator_method or not operator_dict_method:
            raise InvalidFilterError(f"Operator '{filters.operator}' is not supported")

        use_col = field.startswith('extra_')
        field_type = _find_field_type_in_model(model_cls, field)

        if isinstance(field_type, ForeignKey):
            field += '.' + list(field_type.related_columns.keys())[0]

        column = _find_column_in_model(model_cls, field)
        value = _convert_value_by_field_type(model_cls, field, filters.value)

        if filters.operator in FILTER_OPERATORS_SQL_UNPACK:
            unpack_count = FILTER_OPERATORS_SQL_UNPACK[filters.operator]

            if not isinstance(value, (list, tuple)) or len(value) < unpack_count:
                raise InvalidFilterError(f"Operator '{filters.operator}' requires {unpack_count} values in list")

            return cond_query.and_(column.between(*value) if use_col else operator_dict_method(cond_query, field, value))

        return cond_query.and_(operator_method(column, value) if use_col else operator_dict_method(cond_query, field, value))

    if not filters.rules:
        return None

    expressions = []

    for rule in filters.rules:
        expr = build_filter_expression(model_cls, rule)

        if expr is not None:
            expressions.append(expr)

    if not expressions:
        return None

    if len(expressions) == 1:
        return expressions[0]

    if filters.condition == '|':
        return cond_query.or_(*expressions)

    return cond_query.and_(*expressions)


def find_primary_key_field(model_cls: type[Model] | Model) -> str | None:
    for field_name, field_info in model_cls.meta.fields.items():
        if hasattr(field_info, 'primary_key') and field_info.primary_key:
            return field_name

    if 'id' in model_cls.meta.fields:
        return 'id'

    return None


def filter_query(query: QuerySet, filters: str | list | FilterTuple | None, restrict_error: bool = False) -> QuerySet:
    has_filters = filters is not None

    try:
        filters = parse_filter_input(filters)

        if not has_filters and not filters:
            return query

        if has_filters and not filters:
            raise InvalidFilterError("Invalid format of filters")

        filters = validate_filters(query.model_class, filters)
    except InvalidFilterError:
        if has_filters and restrict_error:
            primary_key = find_primary_key_field(query.model_class)

            if primary_key:
                return query.filter({f"{primary_key}__is": None})

        raise

    expression = build_filter_expression(query.model_class, filters)

    if expression is not None:
        query = query.filter(expression)

    return query


def _find_field_type_in_model(model_cls: type[Model], field_path: str) -> type[BaseFieldType]:
    """
        Recursively find a field type in a model by its field path.

        Args:
            model_cls: The model class to search in
            field_path: The field path (e.g. 'contact.company.name')

        Returns:
            The column object

        Raises:
            InvalidFilterError: If the field path is invalid
        """

    field_parts = field_path.split('.')
    current_model = model_cls

    for i, part in enumerate(field_parts):
        if i == 0 and part.startswith('extra_'):
            pass
        elif i == len(field_parts) - 1:
            fields = current_model.meta.fields

            if part in fields:
                return fields.get(part)
            else:
                raise InvalidFilterError(f"Field '{part}' not found in model {current_model.__name__}")
        else:
            if part not in current_model.meta.fields:
                raise InvalidFilterError(f"Field '{part}' not found in model {current_model.__name__}")

            field_info = current_model.meta.fields[part]

            if hasattr(field_info, 'related_model'):
                current_model = field_info.related_model
            elif hasattr(field_info, 'target'):
                current_model = field_info.target
            else:
                raise InvalidFilterError(f"Field '{part}' is not a relationship field")

    raise InvalidFilterError(f"Field '{field_path}' not found")


def _find_column_in_model(model_cls: type[Model], field_path: str) -> Any:
    """
    Recursively find a column in a model by its field path.

    Args:
        model_cls: The model class to search in
        field_path: The field path (e.g. 'contact.company.name')

    Returns:
        The column object

    Raises:
        InvalidFilterError: If the field path is invalid
    """
    field_parts = field_path.split('.')
    current_model = model_cls

    for i, part in enumerate(field_parts):
        if i == 0 and part.startswith('extra_'):
            pass
        elif i == len(field_parts) - 1:
            columns = current_model.table.columns # type: ignore

            if hasattr(columns, part):
                return columns[part]
            else:
                raise InvalidFilterError(f"Field '{part}' not found in model {current_model.__name__}")
        else:
            if part not in current_model.meta.fields:
                raise InvalidFilterError(f"Field '{part}' not found in model {current_model.__name__}")

            field_info = current_model.meta.fields[part]

            if hasattr(field_info, 'related_model'):
                current_model = field_info.related_model
            elif hasattr(field_info, 'target'):
                current_model = field_info.target
            else:
                raise InvalidFilterError(f"Field '{part}' is not a relationship field")

    raise InvalidFilterError(f"Field '{field_path}' not found")


def _convert_value_by_field_type(model_cls: type[Model], field_path: str, value: Any) -> Any:
    """
    Converts a value based on the field type.

    Args:
        model_cls: The model class to search in
        field_path: The field path (e.g. 'contact.company.name')
        value: The value to convert

    Returns:
        The converted value
    """
    field = None
    parts = field_path.split('.')
    current_cls = model_cls

    for part in parts:
        if field_path.startswith('extra_'):
            pass
        else:
            field = current_cls.meta.fields[part]

        if field and hasattr(field, 'target'):
            current_cls = field.target

    if isinstance(field, (DateField, DateTimeField)):
        from datetime import datetime

        return _convert_value(value, lambda val: datetime.fromisoformat(val.replace('Z', '+00:00')))
    elif isinstance(field, IntegerField):
        return _convert_value(value, lambda val: int(val))
    elif isinstance(field, (FloatField, DecimalField)):
        return _convert_value(value, lambda val: float(val))

    return value


def _convert_value(value: Any | None, callback: Callable) -> Any:
    if isinstance(value, str):
        try:
            return callback(value)
        except ValueError:
            return value

    elif isinstance(value, (list, tuple)):
        new_values = []

        for val in value:
            if isinstance(val, str):
                try:
                    val = callback(val)
                except ValueError:
                    pass

            new_values.append(val)

        return new_values

    return value
