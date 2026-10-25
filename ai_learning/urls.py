from django.urls import path
from . import views

urlpatterns = [path('resource/<int:pk>/', views.resource_assistant, name='resource_assistant')]
