# Generated by Django 4.2.3 on 2023-07-31 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiyumi', '0002_alter_volunteer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user/volunteer'),
        ),
    ]
