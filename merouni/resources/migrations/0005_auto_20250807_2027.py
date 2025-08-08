from django.db import migrations
from django.utils.text import slugify

def populate_null_slugs(apps, schema_editor):
    ResourceType = apps.get_model('resources', 'ResourceType')
    for rt in ResourceType.objects.filter(slug__isnull=True):
        rt.slug = slugify(rt.name)
        rt.save()

class Migration(migrations.Migration):
    dependencies = [
        ('resources', '0004_alter_resourcetype_slug'),
    ]
    operations = [
        migrations.RunPython(populate_null_slugs, reverse_code=migrations.RunPython.noop),
    ]