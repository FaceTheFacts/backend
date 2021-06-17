from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("politicians/<int:id>", views.politicians, name="politicians"),
]
