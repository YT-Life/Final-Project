from django.urls import path
from sso import views

app_name = "sso"

urlpatterns = [
   path ('', views.sso_mainpage, name = "mainpage"),
   path ('sso_upload_index/', views.sso_upload_index, name = "upload_index"),
   path ('sso_extract_color/', views.sso_extract_color, name = "extract_color"),
   path ('sso_best_color_palette/', views.sso_best_color_palette, name = "best_color_palette"),
   ]
   
   
   
   
