from django.contrib import admin
from .models import Semester, Subject, ResourceType, Resource

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'description']
    list_filter = ['number']
    search_fields = ['name', 'description']
    ordering = ['number']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'semester']
    list_filter = ['semester']
    search_fields = ['name', 'code', 'description']
    ordering = ['semester', 'name']

@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'resource_type', 'uploaded_by', 'uploaded_at', 'is_active', 'download_count']
    list_filter = ['resource_type', 'subject__semester', 'subject', 'is_active', 'uploaded_at']
    search_fields = ['title', 'description', 'subject__name', 'subject__code']
    readonly_fields = ['uploaded_at', 'updated_at', 'download_count']
    ordering = ['-uploaded_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'subject', 'resource_type')
        }),
        ('File', {
            'fields': ('file',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'uploaded_at', 'updated_at', 'download_count'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

