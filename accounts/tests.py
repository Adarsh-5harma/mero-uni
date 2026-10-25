from django.test import TestCase
from django.urls import reverse

from .models import User


class SignupTests(TestCase):
    def test_login_page_renders(self):
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)

    def test_public_signup_cannot_choose_teacher_role(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newstudent', 'email': 'student@example.com',
            'current_semester': 7, 'role': User.Role.TEACHER,
            'password1': 'Strong-pass-123!', 'password2': 'Strong-pass-123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.get(username='newstudent').role, User.Role.STUDENT)
