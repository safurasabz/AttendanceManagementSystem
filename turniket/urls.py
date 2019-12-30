from django.urls import path
from . import views

app_name = "turniket"

urlpatterns = [
    path('', views.index, name='index'),
    path('filter/', views.filter, name='filter'),
    path('addperm/', views.addperm, name='addperm'),
    path('exportreport/', views.exportreport, name='exportreport'),
    path('addshortday/', views.addshortday, name='addshortday'),
]