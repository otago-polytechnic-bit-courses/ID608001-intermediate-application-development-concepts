from django.urls import path

from . import views

urlpatterns = [
    path("sheds/", views.sheds),
    path("sheds/<int:id>/", views.shed_detail),
    path("sheds/<int:id>/tools/", views.tools),
    path("login/", views.login),
]