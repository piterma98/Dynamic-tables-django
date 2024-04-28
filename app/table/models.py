from typing import Any

from django.apps import apps
from django.db import connections, models


def get_table_model_attrs_from_fields(fields: list[dict[str, str]]) -> dict[str, Any]:
    attrs: dict[str, Any] = {"__module__": "app.table.models"}

    if not fields:
        raise ValueError("Empty fields list passed")

    for field in fields:
        if field["type"] == "string":
            attrs[field["name"]] = models.CharField(null=True, blank=True)
        elif field["type"] == "number":
            attrs[field["name"]] = models.IntegerField(null=True, blank=True)
        elif field["type"] == "boolean":
            attrs[field["name"]] = models.BooleanField(null=True, blank=True)
        else:
            raise ValueError(
                "Unsupported field type. Supported types are 'string', 'number' and 'boolean'."
            )

    return attrs


def create_dynamic_model_class(
    model_name, fields: dict[str, Any]
) -> type[models.Model]:
    class Meta:
        pass

    setattr(Meta, "app_label", "table")
    attrs = {"__module__": __name__, "Meta": Meta}
    if fields:
        attrs = attrs | fields
    return type(model_name, (models.Model,), attrs)


def update_dynamic_model_fields(
    model: type[models.Model], fields: dict[str, Any]
) -> type[models.Model]:
    class Meta:
        pass

    setattr(Meta, "app_label", "table")
    attrs = {"__module__": __name__, "Meta": Meta}
    if fields:
        attrs = attrs | fields
    return type(model.__name__, (model,), attrs)


def get_dynamic_model_by_name(model_name) -> type[models.Model] | None:
    try:
        dynamic_model = apps.get_model("table", model_name)
        return dynamic_model
    except LookupError:
        return None


def create_model_from_dynamic_model(model: type[models.Model]) -> None:
    connection = connections["default"]
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(model)


def update_table_from_dynamic_model(model: type[models.Model]) -> None:
    connection = connections["default"]
    with connection.schema_editor() as schema_editor:
        schema_editor.delete_model(model)
        schema_editor.create_model(model)
