from typing import Any

from edgy import QuerySet, Model
from edgy.core.db.fields import BaseFieldType
from edgy.core.db.models.types import BaseModelType
from fastapi.params import Query, Header

from core.orm.utils import extract_field_names


class FieldSelectorQuery(Query):
    def __init__(self):
        super().__init__(
            default=None,
            title="Fields Selector",
            description="Select which fields to include in the response and use dot notation to select nested fields (ex. 'name,company.name')",
        )


class FieldSelectorHeader(Header):
    def __init__(self):
        super().__init__(
            default=None,
            title="Fields Selector",
            description="Select which fields to include in the response and use dot notation to select nested fields (ex. 'name,company.name')",
            alias="X-Fields",
        )


def parse_field_selector_input(model_cls: type[BaseModelType], fields_expr: str | None) -> dict[str, Any] | None:
    """
    Parse a fields expression into a structured dictionary.
    """
    if not fields_expr or not fields_expr.strip():
        return None

    parts = [part.strip() for part in fields_expr.split(",")]
    result = {"id": True}

    if "+" in parts:
        for field_name, field in model_cls.meta.fields.items():
            _add_field_selector(result, field)

    for part in parts:
        if part == "+":
            continue

        # Handle nested fields (e.g., "owner.name")
        field_path = part.split(".")
        current = result
        current_model = model_cls

        if len(field_path) == 1:
            if field_path[0].startswith("extra_"):
                pass
            else:
                _add_field_selector(current, current_model.meta.fields.get(field_path[0]))
        else:
            parent_path = field_path[:-1]
            last_field = field_path[-1]

            for i, field_name in enumerate(parent_path):
                if current and current_model:
                    field = current_model.meta.fields.get(field_name)

                    if field_name not in current:
                        _add_field_selector(current, field, True)

                    if not isinstance(current.get(field_name), dict):
                        current[field_name] = {'id': True}

                    current = current[field_name]
                    current_model = field.target if field and hasattr(field, "target") else None
                else:
                    break

            if current and current_model:
                field = current_model.meta.fields.get(last_field)

                if field:
                    current[last_field] = True

    return result


def clean_field_names_from_input(model_cls: type[BaseModelType], fields_expr: str | None) -> list[str]:
    fields = [part.strip() for part in fields_expr.split(",")]
    fields_map = parse_field_selector_input(model_cls, fields_expr)
    valid_fields = extract_field_names(fields_map)

    return [field for field in fields if field in valid_fields]


def filter_fields(data: dict, data_obj: Model, fields_map: dict, target: dict) -> None:
    """Filter data recursively based on the field selector."""
    for field_name, field_value in fields_map.items():
        # Si le champ est une structure imbriquée
        if isinstance(field_value, dict):
            if field_name not in target:
                target[field_name] = {}

            if field_name in data and data[field_name] is not None:
                nested_data = data[field_name]
                nested_obj = getattr(data_obj, field_name, None) if data_obj else None

                if isinstance(nested_data, dict):
                    filter_fields(nested_data, nested_obj, field_value, target[field_name])

                elif isinstance(nested_data, list):
                    target[field_name] = []

                    for i, item in enumerate(nested_data):
                        if isinstance(item, dict):
                            target[field_name].append({})
                            nested_item_obj = nested_obj[i] if nested_obj and i < len(nested_obj) else None
                            filter_fields(item, nested_item_obj, field_value, target[field_name][i])
                        else:
                            target[field_name].append(item)

            elif data_obj and hasattr(data_obj, field_name):
                nested_obj = getattr(data_obj, field_name, None)
                if isinstance(nested_obj, Model):
                    nested_data = nested_obj.model_dump()

                    if isinstance(nested_data, dict):
                        filter_fields(nested_data, nested_obj, field_value, target[field_name])

                    elif isinstance(nested_obj, list):
                        target[field_name] = []

                        for i, obj_item in enumerate(nested_obj):
                            if hasattr(obj_item, 'model_dump'):
                                item_data = obj_item.model_dump()
                                target[field_name].append({})
                                filter_fields(item_data, obj_item, field_value, target[field_name][i])
                            else:
                                target[field_name].append(obj_item)
        else:
            if field_name in data:
                target[field_name] = data[field_name]
            elif data_obj and hasattr(data_obj, field_name):
                target[field_name] = getattr(data_obj, field_name)


def filter_selected_fields(item: Model, fields_expr: str | None) -> dict:
    """
    Filters the fields of a model object based on the field selector.

    Note: This function does not optimize the query. To optimize queries,
    use the optimize_query_filter_fields() function directly on the query
    before executing first(), get(), or all().
    """
    map_fields = parse_field_selector_input(item.meta.model, fields_expr)
    item_dump = item.model_dump()

    if map_fields is not None:
        filtered_item = {}
        filter_fields(item_dump, item, map_fields, filtered_item)
        item_dump = filtered_item

    return item_dump


def optimize_query_filter_fields(query: QuerySet, fields_expr: str | None) -> QuerySet:
    """
    Optimizes the query by preloading the requested relationships into the field selector.
    """
    if not fields_expr:
        return query

    model_cls = query.model_class
    map_fields = parse_field_selector_input(model_cls, fields_expr)

    if not map_fields:
        return query

    direct_relations = []

    def collect_relations(fields_map: dict) -> None:
        for field_name, field_value in fields_map.items():
            if isinstance(field_value, dict):
                field = model_cls.meta.fields.get(field_name)

                if field and hasattr(field, "target"):
                    direct_relations.append(field_name)

    collect_relations(map_fields)

    for relation in direct_relations:
        try:
            query = query.select_related(relation)
        except Exception:
            pass

    return query


def _add_field_selector(fields: dict[str, Any], field: BaseFieldType, force: bool = False):
    if field and not field.exclude or force:
        if hasattr(field, "target"):
            field_val = {'id': True}
        else:
            field_val = True

        fields.update({field.name: field_val})
