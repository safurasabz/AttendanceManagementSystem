from django.urls import path
from . import views

app_name = "turniket"

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.filter, name='filter'),
    path('', views.addperm, name='addperm'),
    path('', views.exportreport, name='exportreport'),
]