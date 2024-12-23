from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'category', 'mode', 'is_urgent', 'is_approaching', 'user')
    list_filter = ('category', 'mode', 'is_urgent', 'is_approaching')
    search_fields = ('name', 'description', 'location')
    date_hierarchy = 'date'

