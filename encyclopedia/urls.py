from django.urls import path

from . import views

# app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.getEntry, name="getEntry"),
    path("create", views.create, name="create"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("random", views.randomEntry, name="random"),
    path("search", views.search, name="search"),
]
