from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/<int:user_id>/', views.get_user_info, name='get_user_info'),
    path('drivers/<int:driver_id>/', views.get_driver_info, name='get_driver_info'),
    path('history/<str:entity_type>/<int:entity_id>/', views.get_ride_history, name='get_ride_history'),
    path('create-ride/', views.create_ride, name='create_ride'),
]
