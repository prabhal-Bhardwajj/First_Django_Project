from django.contrib import admin
from .models import Journal

@admin.register(Journal)

class JournalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at','category', 'priority',)  # Customize fields as needed
    list_filter = ('category', 'priority')
    search_fields = ('title', 'content')