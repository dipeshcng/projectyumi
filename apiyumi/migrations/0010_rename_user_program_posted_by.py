# Generated by Django 4.2.3 on 2023-09-21 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiyumi', '0009_program'),
    ]

    operations = [
        migrations.RenameField(
            model_name='program',
            old_name='user',
            new_name='posted_by',
        ),
    ]
