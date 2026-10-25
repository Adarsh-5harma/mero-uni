from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import FileResponse, Http404
from django.conf import settings
import os

from .models import Semester, Subject, Resource, ResourceType
from .models import Bookmark
from .forms import ResourceSubmissionForm

def visible_resources():
    return Resource.objects.filter(is_active=True, status=Resource.Status.APPROVED)

def home(request):
    """Home page view"""
    semesters = Semester.objects.all().order_by('number')
    recent_resources = visible_resources().order_by('-uploaded_at')[:6]
    resource_types = ResourceType.objects.all()
    context = {
        'semesters': semesters,
        'recent_resources': recent_resources,
        'resource_types': resource_types,
    }
    return render(request, 'resources/home.html', context)

def semester_detail(request, semester_number):
    """Semester detail page showing subjects"""
    semester = get_object_or_404(Semester, number=semester_number)
    subjects = semester.subjects.all().order_by('name')
    
    context = {
        'semester': semester,
        'subjects': subjects,
    }
    return render(request, 'resources/semester_detail.html', context)

def subject_detail(request, subject_id):
    """Subject detail page showing resources"""
    subject = get_object_or_404(Subject, id=subject_id)
    resources = visible_resources().filter(subject=subject).order_by('-uploaded_at')
    
    # Filter by resource type if specified
    resource_type = request.GET.get('type')
    if resource_type:
        resources = resources.filter(resource_type__name__icontains=resource_type)
    
    # Pagination
    paginator = Paginator(resources, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all resource types for filtering
    resource_types = ResourceType.objects.all()
    
    context = {
        'subject': subject,
        'page_obj': page_obj,
        'resource_types': resource_types,
        'current_type': resource_type,
    }
    return render(request, 'resources/subject_detail.html', context)

def resource_detail(request, pk):
    """Resource detail page"""
    resource = get_object_or_404(visible_resources(), pk=pk)
    
    is_bookmarked = request.user.is_authenticated and Bookmark.objects.filter(
        user=request.user, resource=resource
    ).exists()
    related_resources = visible_resources().filter(subject=resource.subject).exclude(pk=resource.pk)[:5]
    context = {
        'resource': resource,
        'is_bookmarked': is_bookmarked,
        'related_resources': related_resources,
    }
    return render(request, 'resources/resource_detail.html', context)

def download_resource(request, pk):
    """Download resource file"""
    resource = get_object_or_404(visible_resources(), pk=pk)
    
    # Get file path
    file_path = resource.file.path
    
    if os.path.exists(file_path):
        resource.increment_download_count()
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    else:
        raise Http404("File not found")

def search_resources(request):
    """Search resources"""
    query = request.GET.get('q', '')
    resources = visible_resources()
    
    if query:
        resources = resources.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(subject__name__icontains=query) |
            Q(subject__code__icontains=query) |
            Q(resource_type__name__icontains=query)
        ).distinct()
    
    # Pagination
    paginator = Paginator(resources, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'total_results': resources.count(),
    }
    return render(request, 'resources/search_results.html', context)

def resources_by_type(request, type_slug):
    """Show resources by type"""
    type_mapping = {
        'notes': 'Notes',
        'question-bank': 'Question Bank',
        'lab-solutions': 'Lab Solutions',
        'assignments': 'Assignments',
        'past-papers': 'Past papers',
        'syllabus': 'Syllabus',
    }
    
    type_name = type_mapping.get(type_slug)
    if not type_name:
        raise Http404("Resource type not found")
    
    resource_type = get_object_or_404(ResourceType, name=type_name)
    resources = visible_resources().filter(resource_type=resource_type).order_by('-uploaded_at')
    
    # Filter by semester if specified
    semester = request.GET.get('semester')
    if semester:
        resources = resources.filter(subject__semester__number=semester)
    
    # Pagination
    paginator = Paginator(resources, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all semesters for filtering
    semesters = Semester.objects.all().order_by('number')
    
    context = {
        'resource_type': resource_type,
        'page_obj': page_obj,
        'semesters': semesters,
        'current_semester': semester,
    }
    return render(request, 'resources/resources_by_type.html', context)

def about(request):
    return render(request, 'resources/about.html')


@login_required
def submit_resource(request):
    if request.method == 'POST':
        form = ResourceSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            resource.status = Resource.Status.PENDING
            resource.is_active = True
            resource.save()
            messages.success(request, 'Resource submitted and sent for review.')
            return redirect('profile')
    else:
        form = ResourceSubmissionForm()
    return render(request, 'resources/submit_resource.html', {'form': form})


@login_required
def toggle_bookmark(request, pk):
    if request.method != 'POST':
        raise Http404
    resource = get_object_or_404(visible_resources(), pk=pk)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, resource=resource)
    if not created:
        bookmark.delete()
        messages.info(request, 'Bookmark removed.')
    else:
        messages.success(request, 'Resource bookmarked.')
    return redirect('resource_detail', pk=pk)

