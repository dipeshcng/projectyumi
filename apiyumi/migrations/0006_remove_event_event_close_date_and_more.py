# Generated by Django 4.2.3 on 2023-08-15 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiyumi', '0005_job_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_close_date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='event_date',
        ),
        migrations.AddField(
            model_name='event',
            name='event_end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='event_start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]