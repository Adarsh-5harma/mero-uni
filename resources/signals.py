from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Resource, Subject, ResourceType
from .services import extract_pdf_metadata
import os

@receiver(post_save, sender=Resource)
def auto_extract_metadata(sender, instance, created, **kwargs):
    # Only run when a NEW resource is created, and it has a file
    if created and instance.file:
        
        # Get the absolute path to the PDF
        pdf_path = instance.file.path
        
        # Call the AI Service
        ai_data = extract_pdf_metadata(pdf_path)
        
        if ai_data:
            print(f"🤖 AI Extracted Data for {instance.title}: {ai_data}")
            
            # 1. Map Resource Type (Slug -> DB Object)
            try:
                rt = ResourceType.objects.get(slug=ai_data['resource_type'])
                instance.resource_type = rt
            except ResourceType.DoesNotExist:
                print(f"⚠️ ResourceType slug '{ai_data['resource_type']}' not found in DB.")

            # 2. Map Subject (Name -> DB Object)
            try:
                # We do a case-insensitive search because AI might capitalize differently
                subj = Subject.objects.get(name__iexact=ai_data['subject'])
                instance.subject = subj
            except Subject.DoesNotExist:
                print(f"⚠️ Subject '{ai_data['subject']}' not found in DB.")
            except Subject.MultipleObjectsReturned:
                # If there are two subjects with the same name, just pick the first
                subj = Subject.objects.filter(name__iexact=ai_data['subject']).first()
                instance.subject = subj

            # 3. Save the updated instance without triggering the signal again
            instance.save()
            print("✅ Database updated with AI metadata.")