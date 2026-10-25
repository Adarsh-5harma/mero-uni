from django.contrib import admin
from .models import DocumentAnalysis


@admin.register(DocumentAnalysis)
class DocumentAnalysisAdmin(admin.ModelAdmin):
    list_display = ('resource', 'status', 'model_name', 'processed_at')
    list_filter = ('status', 'model_name')
    search_fields = ('resource__title', 'summary')
    readonly_fields = ('updated_at', 'processed_at')
