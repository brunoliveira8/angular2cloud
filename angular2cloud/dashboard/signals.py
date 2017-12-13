import os
import zipfile
import shutil

import docker

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.signals import request_finished

from .models import Project

#Business Logic
@receiver(post_save, sender=Project, dispatch_uid="save_project")
def on_save_project(sender, **kwargs):
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
        client = docker.from_env()
        name = "{username}_{domain}".format(username=kwargs['instance'].user.username, domain=kwargs['instance'].domain)
        volumes = {dist_folder: {'bind': '/usr/share/nginx/html', "mode": "ro"}}
        environment = {"VIRTUAL_HOST": "{subdomain}.{domain}".format(subdomain=kwargs['instance'].domain, domain="angular2cloud.com")}
        client.containers.run("a2c-angular-nginx", name=name, volumes=volumes, environment=environment, detach=True)
