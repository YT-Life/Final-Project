from django.urls import path
from . import views

app_name ='jun'

urlpatterns = [
    path("", views.main, name='main'),
    path("upload/", views.upload, name='upload'),
    path("extract/", views.extract, name='extract'),
    path("print_extract/", views.print_extract, name='print_extract'),
    path("recommend/", views.recommend, name='recommend'),
]

