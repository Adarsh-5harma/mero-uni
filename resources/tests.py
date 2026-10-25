from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from .models import Bookmark, Resource, ResourceType, Semester, Subject


class ResourceWorkflowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='strong-pass-123')
        self.semester = Semester.objects.create(number=1, name='First Semester')
        self.subject = Subject.objects.create(name='Programming', code='CSC101', semester=self.semester)
        self.resource_type = ResourceType.objects.create(name='Notes', slug='notes')

    def make_resource(self, status=Resource.Status.APPROVED):
        return Resource.objects.create(
            title='Python Notes', subject=self.subject, resource_type=self.resource_type,
            uploaded_by=self.user, status=status,
            file=SimpleUploadedFile('notes.pdf', b'%PDF test'),
        )

    def test_pending_resource_is_not_public(self):
        resource = self.make_resource(Resource.Status.PENDING)
        response = self.client.get(reverse('resource_detail', args=[resource.pk]))
        self.assertEqual(response.status_code, 404)

    def test_authenticated_student_submission_is_pending(self):
        self.client.login(username='student', password='strong-pass-123')
        response = self.client.post(reverse('submit_resource'), {
            'title': 'Algorithms', 'description': 'Revision notes',
            'subject': self.subject.pk, 'resource_type': self.resource_type.pk,
            'file': SimpleUploadedFile('algorithms.pdf', b'%PDF test'),
        })
        self.assertRedirects(response, reverse('profile'))
        submission = Resource.objects.get(title='Algorithms')
        self.assertEqual(submission.status, Resource.Status.PENDING)
        self.assertEqual(submission.uploaded_by, self.user)

    def test_user_can_add_and_remove_bookmark(self):
        resource = self.make_resource()
        self.client.login(username='student', password='strong-pass-123')
        url = reverse('toggle_bookmark', args=[resource.pk])
        self.client.post(url)
        self.assertTrue(Bookmark.objects.filter(user=self.user, resource=resource).exists())
        self.client.post(url)
        self.assertFalse(Bookmark.objects.filter(user=self.user, resource=resource).exists())

    def test_submission_rejects_unsupported_file(self):
        self.client.login(username='student', password='strong-pass-123')
        response = self.client.post(reverse('submit_resource'), {
            'title': 'Unsafe', 'subject': self.subject.pk,
            'resource_type': self.resource_type.pk,
            'file': SimpleUploadedFile('program.exe', b'not allowed'),
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Upload a PDF, Word, PowerPoint, or text document.')

    def test_public_resource_navigation_and_search(self):
        resource = self.make_resource()
        self.assertEqual(self.client.get(reverse('home')).status_code, 200)
        self.assertEqual(self.client.get(reverse('semester_detail', args=[1])).status_code, 200)
        self.assertEqual(self.client.get(reverse('subject_detail', args=[self.subject.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse('resource_detail', args=[resource.pk])).status_code, 200)
        search = self.client.get(reverse('search_resources'), {'q': 'Python'})
        self.assertContains(search, resource.title)

    def test_download_responds_and_increments_counter(self):
        resource = self.make_resource()
        response = self.client.get(reverse('download_resource', args=[resource.pk]))
        self.assertEqual(response.status_code, 200)
        list(response.streaming_content)
        resource.refresh_from_db()
        self.assertEqual(resource.download_count, 1)

    def test_profile_and_submission_pages_render_when_logged_in(self):
        self.client.login(username='student', password='strong-pass-123')
        self.assertEqual(self.client.get(reverse('profile')).status_code, 200)
        self.assertEqual(self.client.get(reverse('submit_resource')).status_code, 200)
