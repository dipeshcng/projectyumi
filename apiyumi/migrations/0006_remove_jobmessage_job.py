# Generated by Django 4.2.3 on 2023-09-21 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiyumi', '0005_remove_jobmessage_user_jobmessage_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobmessage',
            name='job',
        ),
    ]