from django.urls import path
from . import views

app_name = 'lyt'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('img_upload/', views.img_upload, name='img_upload'),
    path('upload/', views.upload, name="upload"),
    path('mix_color/', views.mix_color, name="mix_color")
]
