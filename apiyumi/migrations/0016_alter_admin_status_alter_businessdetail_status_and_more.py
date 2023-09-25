# Generated by Django 4.2.3 on 2023-09-25 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiyumi', '0015_rename_resume_job_applied_graduates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Disabled', 'Disabled')], default='Active', max_length=50),
        ),
        migrations.AlterField(
            model_name='businessdetail',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Disabled', 'Disabled')], default='Active', max_length=50),
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Disabled', 'Disabled')], default='Active', max_length=50),
        ),
        migrations.AlterField(
            model_name='graduatesdetail',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Disabled', 'Disabled')], default='Active', max_length=50),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Disabled', 'Disabled')], default='Active', max_length=50),
        ),
        migrations.AlterField(
            model_name='jobmessage',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Disabled', 'Disabled')], default='Active', max_length=50),
        ),
        migrations.AlterField(
            model_name='program',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Disabled', 'Disabled')], default='Active', max_length=50),
        ),
        migrations.AlterField(
            model_name='programdocument',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Disabled', 'Disabled')], default='Active', max_length=50),
        ),
        migrations.AlterField(
            model_name='resume',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Disabled', 'Disabled')], default='Active', max_length=50),
        ),
        migrations.AlterField(
            model_name='role',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Disabled', 'Disabled')], default='Active', max_length=50),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Active', 'Active'), ('Disabled', 'Disabled')], default='Active', max_length=50),
        ),
    ]
