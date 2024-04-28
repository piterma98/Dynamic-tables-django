from unittest.mock import ANY

import pytest
from django.db import models

from table.models import (
    create_dynamic_model_class,
    get_dynamic_model_by_name,
    get_table_model_attrs_from_fields,
    update_dynamic_model_fields,
)


def test_get_table_model_attrs_from_fields() -> None:
    fields = [
        {"name": "name", "type": "string"},
        {"name": "price", "type": "number"},
        {"name": "is_valid", "type": "boolean"},
    ]
    model_fields = get_table_model_attrs_from_fields(fields)
    assert {
        "__module__": "app.table.models",
        "name": ANY,
        "price": ANY,
        "is_valid": ANY,
    } == model_fields


def test_get_table_model_attrs_from_fields_unsupported_field() -> None:
    fields = [
        {"name": "name", "type": "dict"},
    ]
    with pytest.raises(ValueError):
        get_table_model_attrs_from_fields(fields)


def test_get_table_model_attrs_from_fields_empty_fields() -> None:
    with pytest.raises(ValueError):
        get_table_model_attrs_from_fields([])


@pytest.mark.django_db
def test_create_dynamic_model_class() -> None:
    fields = [
        {"name": "name", "type": "string"},
        {"name": "price", "type": "number"},
        {"name": "is_valid", "type": "boolean"},
    ]
    model_fields = get_table_model_attrs_from_fields(fields)
    model = create_dynamic_model_class(model_name="Testing", fields=model_fields)
    assert str(
        model._meta.fields
        == "(<django.db.models.fields.BigAutoField: id>, <django.db.models.fields.CharField: name>, <django.db.models.fields.IntegerField: price>, <django.db.models.fields.BooleanField: is_valid>)"
    )
    assert model.__name__ == "Testing"
    assert model.__doc__ == "Testing(id, name, price, is_valid)"
    assert isinstance(model, models.base.ModelBase)


@pytest.mark.django_db
def test_get_dynamic_model_by_name() -> None:
    fields = [
        {"name": "name", "type": "string"},
        {"name": "price", "type": "number"},
        {"name": "is_valid", "type": "boolean"},
    ]
    model_fields = get_table_model_attrs_from_fields(fields)
    model = create_dynamic_model_class(model_name="DynamicTable", fields=model_fields)
    dynamic_model = get_dynamic_model_by_name("DynamicTable")
    assert model == dynamic_model


@pytest.mark.django_db
def test_get_dynamic_model_by_name_error() -> None:
    dynamic_model = get_dynamic_model_by_name("Error")
    assert dynamic_model is None


@pytest.mark.django_db
def test_update_dynamic_model_fields() -> None:
    fields = [
        {"name": "name", "type": "string"},
        {"name": "price", "type": "number"},
        {"name": "is_valid", "type": "boolean"},
    ]
    model_fields = get_table_model_attrs_from_fields(fields)
    model = create_dynamic_model_class(
        model_name="TableWithNewField", fields=model_fields
    )
    new_field = [{"name": "status", "type": "string"}]
    model = update_dynamic_model_fields(
        model, get_table_model_attrs_from_fields(new_field)
    )
    assert (
        model.__doc__
        == "TableWithNewField(id, name, price, is_valid, tablewithnewfield_ptr, status)"
    )
