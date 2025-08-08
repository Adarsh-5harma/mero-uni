from django.db import migrations
from django.utils.text import slugify

def populate_slugs(apps, schema_editor):
    ResourceType = apps.get_model('resources', 'ResourceType')
    for rt in ResourceType.objects.all():
        rt.slug = slugify(rt.name)
        rt.save()

class Migration(migrations.Migration):
    dependencies = [
        ('resources', '0002_resourcetype_slug'),  # Adjust if different
    ]
    operations = [
        migrations.RunPython(populate_slugs, reverse_code=migrations.RunPython.noop),
    ]