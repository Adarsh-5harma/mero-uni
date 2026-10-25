from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        TEACHER = 'teacher', 'Teacher'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    current_semester = models.PositiveSmallIntegerField(
        choices=[(i, f'Semester {i}') for i in range(1, 9)],
        null=True,
        blank=True,
    )

    @property
    def can_moderate_resources(self):
        return self.is_staff or self.role == self.Role.TEACHER
