# Generated by Django 4.2.3 on 2023-09-27 07:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiyumi', '0017_alter_businessdetail_business_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graduatesdetail',
            name='phone',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
