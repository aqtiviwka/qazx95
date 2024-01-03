from django.urls import path
from . import views


urlpatterns = [
    path('', views.download_data, name='download_data'),
    path('show_data/', views.show_data, name='show_data'),
    path('error_format_file/', views.error_of_format_file, name='error_of_format_file'),
    path('error_format_data/', views.error_of_format_data, name='error_of_format_data'),
    path('error_keys/', views.error_of_keys, name='error_keys'),
    path('everything_is_correct/', views.everything_is_correct, name='OK')

]