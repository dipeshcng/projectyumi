# Generated by Django 4.2.3 on 2023-09-21 04:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apiyumi', '0008_remove_job_message_jobmessage_job'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Disabled', 'Disabled')], default='Pending', max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('document', models.FileField(blank=True, null=True, upload_to='')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('registered_by', models.ManyToManyField(blank=True, related_name='program_registered_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]