from django.urls import path
from . import views

app_name = 'jcc'

urlpatterns = [
    path("", views.main, name="main"),
]