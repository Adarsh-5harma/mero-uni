from pathlib import Path

from django import forms
from django.core.exceptions import ValidationError

from .models import Resource


class ResourceSubmissionForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ('title', 'description', 'subject', 'resource_type', 'file')
        widgets = {'description': forms.Textarea(attrs={'rows': 4})}

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        allowed_extensions = {'.pdf', '.doc', '.docx', '.ppt', '.pptx', '.txt'}
        if Path(uploaded_file.name).suffix.lower() not in allowed_extensions:
            raise ValidationError('Upload a PDF, Word, PowerPoint, or text document.')
        if uploaded_file.size > 20 * 1024 * 1024:
            raise ValidationError('The file must be 20 MB or smaller.')
        return uploaded_file
