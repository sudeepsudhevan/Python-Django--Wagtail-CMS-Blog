# Generated by Django 5.1.4 on 2025-01-15 03:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpages', '0010_blogdetail_author'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='locked',
            field=models.BooleanField(default=False, editable=False, verbose_name='locked'),
        ),
        migrations.AddField(
            model_name='author',
            name='locked_at',
            field=models.DateTimeField(editable=False, null=True, verbose_name='locked at'),
        ),
        migrations.AddField(
            model_name='author',
            name='locked_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locked_%(class)ss', to=settings.AUTH_USER_MODEL, verbose_name='locked by'),
        ),
    ]
