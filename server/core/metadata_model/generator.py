from edgy import Model
import re

from edgy.core.db.fields import BaseFieldType

from core import context
from core.api_route_model.params import find_primary_key_field
from core.api_route_model.params.filter import get_filter_operators
from schemas.dataset import MetadataModel, MetadataField


class MetadataFieldError(Exception):...


def generate_metadata_name(model_cls: type[Model] | Model) -> str:
    class_name = model_cls.__name__
    return re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()


async def generate_metadata_model(model_cls: Model) -> MetadataModel:
    class_name = model_cls.__name__
    name = generate_metadata_name(model_cls)
    label = re.sub(r'(?<!^)(?=[A-Z])', ' ', class_name)
    label_plural = f"{label}s"

    if hasattr(model_cls.Meta, 'label'):
        label = model_cls.Meta.label

    if hasattr(model_cls.Meta, 'label_plural'):
        label_plural = model_cls.Meta.label_plural

    fields = await generate_metadata_fields(model_cls)
    has_searchable_fields = False
    for field in fields.values():
        if field.searchable:
            has_searchable_fields = True
            break

    metadata = MetadataModel(
        name=name,
        label=label,
        label_plural=label_plural,
        searchable=has_searchable_fields,
        fields=fields,
    )

    return metadata


async def generate_metadata_fields(model_cls: Model) -> dict[str, MetadataField]:
    fields = {}
    for field_name, field_info in model_cls.meta.fields.items():
        if not field_info.exclude:
            fields[field_name] = generate_metadata_field(model_cls, field_info)

    return fields


def generate_metadata_field_type(field: BaseFieldType) -> str:
    field_type = type(field).__name__

    if field_type == 'FieldFactoryMeta':
        field_type = field.__name__

    field_type = field_type[:-5] if field_type.endswith("Field") else field_type

    return re.sub(r'(?<!^)(?=[A-Z])', '_', field_type).lower()


def generate_metadata_field(model_cls: Model, field: BaseFieldType) -> MetadataField:
    name_parts = field.name.split('_')
    label = name_parts[0].capitalize()
    if len(name_parts) > 1:
        label = ' '.join([name_parts[0].capitalize()] + [word.lower() for word in name_parts[1:]])

    field_type = generate_metadata_field_type(field)
    readonly = field.read_only
    has_default = field.default is not None
    required = not field.null and not field.read_only

    if find_primary_key_field(model_cls) == field.name:
        readonly = True

    target_model = field.target if field and hasattr(field, "target") else None
    label = field.label if field and hasattr(field, "label") else label
    filter_operators = get_filter_operators(field)
    searchable = field.searchable if field and hasattr(field, "searchable") else len(filter_operators) > 0

    if searchable and not filter_operators:
        raise MetadataFieldError(f"Metadata field {field.name} must have a filter operator if searchable is enabled")

    return MetadataField(
        name=field.name,
        label=label,
        type=field_type,
        readonly=readonly,
        required=required and not readonly and not has_default,
        searchable=searchable,
        extra=False,
        filter_operators=filter_operators,
        target=generate_metadata_name(target_model) if target_model else None
    )
