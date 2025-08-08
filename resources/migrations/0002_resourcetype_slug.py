from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('resources', '0001_initial'),
    ]
    operations = [
        migrations.AddField(
            model_name='ResourceType',
            name='slug',
            field=models.SlugField(max_length=50, unique=True, null=True),  # Allow null
        ),
    ]