# Generated by Django 5.1.4 on 2025-01-13 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_homepagegalleryimage_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepagegalleryimage',
            name='caption',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
