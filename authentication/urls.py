from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('validate-username/', views.validate_username, name='validate_username'),
]



