from django.urls import path
from . import views

urlpatterns = [
    path("",views.index),
    path("login",views.login),
    path('login_form', views.login_form),
    path("registration",views.registration),
    path('register_form', views.register_form),
    path("logout",views.logout),
    path("trips/new",views.create_trip),
    path("trips/new/create_trip_form", views.create_trip_form),
    path("delete/<int:id>",views.delete_trip),
    path("trips/<int:id>",views.read),
    path("join/<int:id>",views.join),
    path("cancel_join/<int:id>",views.cancel_join),
    path("trips/edit/<int:id>",views.edit_trip),
    path("trips/edit/<int:id>/edit_trip_form",views.edit_trip_form),
]