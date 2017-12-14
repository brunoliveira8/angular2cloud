import os


from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.signals import request_finished

from .models import Project
from .utils import run_container, remove_container, unzip, remove_project_folder

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
    project = kwargs['instance']
    update_fields = kwargs['update_fields']
    created = kwargs['created']

    if created:
        unzip(project)
        run_container(project)

    else:
        if update_fields and 'status' not in update_fields:
            unzip(project)
            if project.status == 'RN':
                restart_container(project)


@receiver(post_delete, sender=Project, dispatch_uid="delete_project")
def on_delete_project(sender, **kwargs):
    project = kwargs['instance']
    remove_container(project)
    remove_project_folder(project)


