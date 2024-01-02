from django.urls import path
from . import views


urlpatterns = [
    path('', views.download_data, name='download_data'),
    path('show_data/', views.show_data, name='show_data')
]