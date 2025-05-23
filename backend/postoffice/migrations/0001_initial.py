# Generated by Django 5.0 on 2025-04-06 17:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_from', models.EmailField(max_length=254)),
                ('mail_to', models.TextField()),
                ('mail_cc', models.CharField(blank=True, max_length=1000, null=True)),
                ('mail_bcc', models.CharField(blank=True, max_length=1000, null=True)),
                ('subject', models.CharField(max_length=500)),
                ('message', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('draft', 'Draft'), ('sent', 'Sent'), ('failed', 'Failed')], default='draft', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('is_now', models.BooleanField(default=True)),
                ('action_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
