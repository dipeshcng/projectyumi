# Generated by Django 4.2.3 on 2023-09-21 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apiyumi', '0007_job_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='message',
        ),
        migrations.AddField(
            model_name='jobmessage',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apiyumi.job'),
        ),
    ]
