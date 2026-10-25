from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import User
from resources.models import Resource, ResourceType, Semester, Subject
from .models import DocumentAnalysis
from .services import AIServiceError, extract_resource_text, generate_summary


class AILearningTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='learner', password='strong-pass-123')
        semester = Semester.objects.create(number=1, name='First Semester')
        subject = Subject.objects.create(name='AI', code='AI101', semester=semester)
        resource_type = ResourceType.objects.create(name='Notes', slug='notes')
        self.resource = Resource.objects.create(
            title='AI Notes', subject=subject, resource_type=resource_type,
            uploaded_by=self.user, status=Resource.Status.APPROVED,
            file=SimpleUploadedFile('ai.txt', b'Machine learning uses data to learn useful patterns.'),
        )

    def test_text_extraction(self):
        self.assertIn('Machine learning', extract_resource_text(self.resource))

    def test_assistant_requires_login(self):
        response = self.client.get(reverse('resource_assistant', args=[self.resource.pk]))
        self.assertEqual(response.status_code, 302)

    @override_settings(GEMINI_API_KEY='test-key')
    @patch('ai_learning.views.generate_summary', return_value='A concise AI summary.')
    def test_summary_is_stored(self, mocked_summary):
        self.client.login(username='learner', password='strong-pass-123')
        response = self.client.post(reverse('resource_assistant', args=[self.resource.pk]))
        self.assertRedirects(response, reverse('resource_assistant', args=[self.resource.pk]))
        analysis = DocumentAnalysis.objects.get(resource=self.resource)
        self.assertEqual(analysis.status, DocumentAnalysis.Status.COMPLETED)
        self.assertEqual(analysis.summary, 'A concise AI summary.')
        mocked_summary.assert_called_once()

    @override_settings(GEMINI_API_KEY='')
    def test_missing_api_key_has_safe_error(self):
        with self.assertRaisesMessage(AIServiceError, 'Gemini is not configured'):
            generate_summary('content')
