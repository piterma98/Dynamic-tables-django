import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from table.models import (
    create_dynamic_model_class,
    create_model_from_dynamic_model,
    get_table_model_attrs_from_fields,
)


@pytest.mark.django_db
def test_generate_dynamic_model_view(client: APIClient) -> None:
    data = {
        "name": "mytable",
        "fields": [
            {"name": "columnstr", "type": "string"},
            {"name": "columnnr", "type": "number"},
            {"name": "columnbool", "type": "boolean"},
        ],
    }

    url = reverse("generate-dynamic-model")
    response = client.post(url, data=data, format="json")

    assert response.json() == {
        "table_name": "mytable",
        "fields": [
            {"name": "columnstr", "type": "string"},
            {"name": "columnnr", "type": "number"},
            {"name": "columnbool", "type": "boolean"},
        ],
    }
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_generate_dynamic_model_view_error(client: APIClient) -> None:
    data = {
        "name": "mytable",
        "fields": [
            {"name": "columnstr", "type": "test"},
        ],
    }

    url = reverse("generate-dynamic-model")
    response = client.post(url, data=data, format="json")

    assert response.json() == {
        "error": "Unsupported field type. Supported types are 'string', 'number' and 'boolean'."
    }
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_generate_dynamic_model_view_serializer_error(client: APIClient) -> None:
    data = {
        "test": "mytable",
    }

    url = reverse("generate-dynamic-model")
    response = client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_dynamic_model(client: APIClient) -> None:
    fields = [
        {"name": "name", "type": "string"},
        {"name": "price", "type": "number"},
        {"name": "is_valid", "type": "boolean"},
    ]
    model_fields = get_table_model_attrs_from_fields(fields)
    model = create_dynamic_model_class(
        model_name="TableWithNewField", fields=model_fields
    )
    create_model_from_dynamic_model(model)
    new_field = {"fields": [{"type": "string", "name": "status"}]}

    url = reverse("update-dynamic-model", kwargs={"id": model.__name__})
    response = client.put(url, data=new_field, format="json")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_add_row(client: APIClient) -> None:
    fields = [
        {"name": "name", "type": "string"},
        {"name": "price", "type": "number"},
        {"name": "is_valid", "type": "boolean"},
    ]
    model_fields = get_table_model_attrs_from_fields(fields)
    model = create_dynamic_model_class(
        model_name="TableWithNewField", fields=model_fields
    )
    create_model_from_dynamic_model(model)
    data = [
        {"name": "name", "value": "test"},
        {"name": "price", "value": 500},
        {"name": "is_valid", "value": "True"},
    ]

    url = reverse("add-row", kwargs={"id": model.__name__})
    response = client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": 1,
        "name": "test",
        "price": "500",
        "is_valid": "True",
    }


@pytest.mark.django_db
def test_list_rows(client: APIClient) -> None:
    fields = [
        {"name": "name", "type": "string"},
        {"name": "price", "type": "number"},
        {"name": "is_valid", "type": "boolean"},
    ]
    model_fields = get_table_model_attrs_from_fields(fields)
    model = create_dynamic_model_class(
        model_name="TableWithNewField", fields=model_fields
    )
    create_model_from_dynamic_model(model)
    model(name="test", price=500, is_valid=True).save()
    model(name="text", price=2137, is_valid=False).save()
    model(name="heheszky", price=1337, is_valid=True).save()

    url = reverse("list-rows", kwargs={"id": "TableWithNewField"})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"id": 1, "name": "test", "price": 500, "is_valid": True},
        {"id": 2, "name": "text", "price": 2137, "is_valid": False},
        {"id": 3, "name": "heheszky", "price": 1337, "is_valid": True},
    ]
