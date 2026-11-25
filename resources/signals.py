from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Resource, Subject, ResourceType
from .services import extract_pdf_metadata
import requests
import os

@receiver(post_save, sender=Resource)
def auto_extract_metadata(sender, instance, created, **kwargs):
    if created and instance.file:
        pdf_path = instance.file.path
        
        # 1. Get Metadata from AI
        ai_data = extract_pdf_metadata(pdf_path)
        
        if ai_data:
            print(f"🤖 AI Extracted Data: {ai_data}")
            
            try:
                rt = ResourceType.objects.get(slug=ai_data['resource_type'])
                instance.resource_type = rt
            except ResourceType.DoesNotExist:
                print(f"⚠️ ResourceType '{ai_data['resource_type']}' not found.")

            try:
                subj = Subject.objects.get(name__iexact=ai_data['subject'])
                instance.subject = subj
            except Subject.DoesNotExist:
                print(f"⚠️ Subject '{ai_data['subject']}' not found.")

            # Save the DB record first so it has an ID
            instance.save()
            
            # 2. Send to Vector DB (ChromaDB)
            print("📥 Sending to Vector DB...")
            try:
                # We will add this endpoint to FastAPI in a second
                requests.post(
                    "http://127.0.0.1:8000/ingest",
                    json={"file_path": pdf_path, "resource_id": instance.pk},
                    timeout=120
                )
                print("✅ Vector DB updated.")
            except Exception as e:
                print(f"❌ Vector DB Error: {e}")