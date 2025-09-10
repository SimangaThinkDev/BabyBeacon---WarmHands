from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('handle_reg', views.handle_reg, name="handle_reg"),
    path('users/<int:user_id>/', views.get_user_info, name='get_user_info'),
    path('drivers/<int:driver_id>/', views.get_driver_info, name='get_driver_info'),
    path('history/<str:entity_type>/<int:entity_id>/', views.get_ride_history, name='get_ride_history'),
    path('create-ride/', views.create_ride, name='create_ride'),
]
