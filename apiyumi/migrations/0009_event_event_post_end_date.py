# Generated by Django 4.2.3 on 2023-08-18 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiyumi', '0008_alter_admin_user_alter_businessdetail_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_post_end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]