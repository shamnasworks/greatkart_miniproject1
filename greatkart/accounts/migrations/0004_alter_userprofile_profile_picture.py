# Generated by Django 5.1.6 on 2025-03-08 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_account_groups_remove_account_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='userprofile/'),
        ),
    ]
