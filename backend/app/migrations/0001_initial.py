# Generated by Django 5.0 on 2025-04-06 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(blank=True, max_length=100, null=True)),
                ('subject', models.CharField(blank=True, max_length=100, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('resolved', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Contact Us',
                'ordering': ['-created_on'],
            },
        ),
    ]
