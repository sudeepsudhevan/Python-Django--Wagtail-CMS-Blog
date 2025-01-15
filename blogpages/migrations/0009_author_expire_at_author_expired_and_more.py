# Generated by Django 5.1.4 on 2025-01-15 03:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpages', '0008_alter_blogdetail_body'),
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='expire_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='expiry date/time'),
        ),
        migrations.AddField(
            model_name='author',
            name='expired',
            field=models.BooleanField(default=False, editable=False, verbose_name='expired'),
        ),
        migrations.AddField(
            model_name='author',
            name='first_published_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='first published at'),
        ),
        migrations.AddField(
            model_name='author',
            name='go_live_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='go live date/time'),
        ),
        migrations.AddField(
            model_name='author',
            name='has_unpublished_changes',
            field=models.BooleanField(default=False, editable=False, verbose_name='has unpublished changes'),
        ),
        migrations.AddField(
            model_name='author',
            name='last_published_at',
            field=models.DateTimeField(editable=False, null=True, verbose_name='last published at'),
        ),
        migrations.AddField(
            model_name='author',
            name='latest_revision',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.revision', verbose_name='latest revision'),
        ),
        migrations.AddField(
            model_name='author',
            name='live',
            field=models.BooleanField(default=True, editable=False, verbose_name='live'),
        ),
        migrations.AddField(
            model_name='author',
            name='live_revision',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.revision', verbose_name='live revision'),
        ),
    ]
