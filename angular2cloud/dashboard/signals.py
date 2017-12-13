import os
import zipfile
import shutil

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.signals import request_finished

from .models import Project
from .utils import run_container

#Business Logic
@receiver(post_save, sender=Project, dispatch_uid="save_project")
def on_save_project(sender, **kwargs):
    ''' This handler is called in tree ways:
        1. When a new project is created.
        2. When a new file is updated.
        3. When the status is changed
    '''

    '''
        In case of status is present in update_fields, this lines of code should not be called
        because unzip or remove the dist folder is not necessary. update_fields is passed in views.ProjectActivate.post
    '''
    if kwargs['update_fields'] and 'status' not in kwargs['update_fields']:
        path = os.path.join(settings.MEDIA_ROOT, kwargs['instance'].user.username, kwargs['instance'].domain)
        dist_folder = os.path.join(path, 'dist')
        dist_file = os.path.join(path, "dist.zip")

        if os.path.isdir(dist_folder):
            shutil.rmtree(os.path.join(path, 'dist'))

        if os.path.exists(dist_file):
            zip_ref = zipfile.ZipFile(dist_file, 'r')
            zip_ref.extractall(path)
            zip_ref.close()

        if kwargs['created']:
            run_container(kwargs['instance'])
        else:
            if kwargs['instance'].status == 'RN':
                restart_container(kwargs['instance'])
