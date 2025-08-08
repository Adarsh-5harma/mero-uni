from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('semester/<int:semester_number>/', views.semester_detail, name='semester_detail'),
    path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('resource/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('download/<int:pk>/', views.download_resource, name='download_resource'),
    path('search/', views.search_resources, name='search_resources'),
    path('type/<str:type_slug>/', views.resources_by_type, name='resources_by_type'),
    path('about/', views.about, name='about'),
]

