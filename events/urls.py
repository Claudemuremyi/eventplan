from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('events/', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('edit/<int:pk>/', views.event_edit, name='event_edit'),
    path('delete/<int:pk>/', views.event_delete, name='event_delete'),
    path('search/', views.event_search, name='event_search'),
    path('stats/', views.event_stats, name='event_stats'),
]

