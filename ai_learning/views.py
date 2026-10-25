from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from resources.models import Resource
from .models import DocumentAnalysis
from .services import AIServiceError, extract_resource_text, generate_summary


@login_required
def resource_assistant(request, pk):
    resource = get_object_or_404(Resource, pk=pk, is_active=True, status=Resource.Status.APPROVED)
    analysis, _ = DocumentAnalysis.objects.get_or_create(resource=resource)
    if request.method == 'POST':
        try:
            text = analysis.extracted_text or extract_resource_text(resource)
            analysis.extracted_text = text
            analysis.status = DocumentAnalysis.Status.EXTRACTED
            analysis.error_message = ''
            analysis.save()
            analysis.summary = generate_summary(text)
            analysis.status = DocumentAnalysis.Status.COMPLETED
            analysis.model_name = settings.GEMINI_MODEL
            analysis.processed_at = timezone.now()
            analysis.save()
            messages.success(request, 'AI summary generated successfully.')
        except AIServiceError as exc:
            analysis.status = DocumentAnalysis.Status.FAILED
            analysis.error_message = str(exc)
            analysis.save(update_fields=['status', 'error_message', 'updated_at'])
            messages.error(request, str(exc))
        return redirect('resource_assistant', pk=pk)
    return render(request, 'ai_learning/resource_assistant.html', {'resource': resource, 'analysis': analysis})
