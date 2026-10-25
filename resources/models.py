from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse
from django.db.models import F

class Semester(models.Model):
    number = models.IntegerField(unique=True,
                                 choices=[(i, f"Semester {i}") for i in range(1, 9)]
                                 )
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['number']
    
    def __str__(self):
        return f"{self.name}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class ResourceType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Resource(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending review'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='resources')
    resource_type = models.ForeignKey(ResourceType, on_delete=models.CASCADE, related_name='resources')
    file = models.FileField(upload_to='resources/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_resources')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.APPROVED)
    moderation_note = models.TextField(blank=True)
    download_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.title} - {self.subject.name}"
    
    def get_absolute_url(self):
        return reverse('resource_detail', kwargs={'pk': self.pk})
    
    def increment_download_count(self):
        Resource.objects.filter(pk=self.pk).update(download_count=F('download_count') + 1)
        self.refresh_from_db(fields=['download_count'])


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'resource'], name='unique_resource_bookmark')
        ]

    def __str__(self):
        return f'{self.user} bookmarked {self.resource}'

