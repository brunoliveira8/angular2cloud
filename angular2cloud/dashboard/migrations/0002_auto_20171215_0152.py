# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-15 01:52
from __future__ import unicode_literals

import dashboard.models
import dashboard.storage
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='domain',
            field=models.SlugField(help_text='Your domain must be unique. Your project will be available at yourdomain.angular2cloud.com', unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(help_text='You can choose any name for your project.', max_length=120),
        ),
        migrations.AlterField(
            model_name='project',
            name='source',
            field=models.FileField(help_text='Upload the dist folder of your Angular project as a zip file.', storage=dashboard.storage.OverwriteStorage(), upload_to=dashboard.models.user_directory_path, validators=[dashboard.models.validate_slug_blacklist, django.core.validators.FileExtensionValidator(allowed_extensions=['zip'])]),
        ),
    ]
