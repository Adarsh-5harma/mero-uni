from django.db import models

from resources.models import Resource


class DocumentAnalysis(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', 'Not started'
        EXTRACTED = 'extracted', 'Text extracted'
        COMPLETED = 'completed', 'Summary ready'
        FAILED = 'failed', 'Failed'

    resource = models.OneToOneField(Resource, on_delete=models.CASCADE, related_name='ai_analysis')
    extracted_text = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.NOT_STARTED)
    error_message = models.CharField(max_length=500, blank=True)
    model_name = models.CharField(max_length=100, blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'AI analysis: {self.resource.title}'
