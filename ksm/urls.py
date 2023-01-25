from django.urls import path
from . import views

app_name = 'ksm'

urlpatterns = [
    path("index/", views.index, name='index'),
    path("img_upload", views.img_upload, name='img_upload'),
    path("color_extract", views.color_extract, name = "color_extract"),
    path("print_extract", views.print_extract, name = "print_extract"),
    path("recommend", views.recommend, name = "recommend")
]