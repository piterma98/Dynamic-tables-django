from django.urls import path

from table import views

urlpatterns = [
    path("", views.generate_dynamic_model, name="generate-dynamic-model"),
    path("<str:id>", views.update_dynamic_model, name="update-dynamic-model"),
    path("<str:id>/row", views.add_row, name="add-row"),
    path("<str:id>/rows", views.list_rows, name="list-rows"),
]
