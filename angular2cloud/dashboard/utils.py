import os
import zipfile
import shutil

import docker

from django.conf import settings

def run_container(project):
    path = os.path.join(settings.MEDIA_ROOT, project.user.username, project.domain)
    dist_folder = os.path.join(path, 'dist')
    client = docker.from_env()
    name = "{username}_{domain}".format(username=project.user.username, domain=project.domain)
    volumes = {dist_folder: {'bind': '/usr/share/nginx/html', "mode": "ro"}}
    environment = {
        "VIRTUAL_HOST": "{subdomain}.{domain}".format(subdomain=project.domain, domain="angular2cloud.com"),
        "LETSENCRYPT_HOST": "{subdomain}.{domain}".format(subdomain=project.domain, domain="angular2cloud.com"),
        "LETSENCRYPT_EMAIL": "cloudangular@gmail.com"
    }
    network = "reverse-proxy"
    client.containers.run("a2c-angular-nginx",
        name=name,
        volumes=volumes,
        environment=environment,
        network=network,
        detach=True
    )


def restart_container(project):
    client = docker.from_env()
    ct = client.containers.get("{username}_{domain}".format(username=project.user.username, domain=project.domain))
    ct.resart()


def start_container(project):
    client = docker.from_env()
    ct = client.containers.get("{username}_{domain}".format(username=project.user.username, domain=project.domain))
    ct.start()


def stop_container(project):
    client = docker.from_env()
    ct = client.containers.get("{username}_{domain}".format(username=project.user.username, domain=project.domain))
    ct.stop()


def remove_container(project):
    try:
        client = docker.from_env()
        ct = client.containers.get("{username}_{domain}".format(username=project.user.username, domain=project.domain))
        ct.stop()
        ct.remove()
    except:
        pass


def unzip(project):
    path = os.path.join(settings.MEDIA_ROOT, project.user.username, project.domain)
    dist_folder = os.path.join(path, 'dist')
    dist_file = os.path.join(path, "dist.zip")

    if os.path.isdir(dist_folder):
        shutil.rmtree(os.path.join(path, 'dist'))

    if os.path.exists(dist_file):
        zip_ref = zipfile.ZipFile(dist_file, 'r')
        zip_ref.extractall(path)
        zip_ref.close()


def remove_project_folder(project):
     project_folder = os.path.join(settings.MEDIA_ROOT, project.user.username, project.domain)
     if os.path.isdir(project_folder):
            shutil.rmtree(project_folder)