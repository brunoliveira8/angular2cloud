import os
import docker

from django.conf import settings

def run_container(project):
    path = os.path.join(settings.MEDIA_ROOT, project.user.username, project.domain)
    dist_folder = os.path.join(path, 'dist')
    client = docker.from_env()
    name = "{username}_{domain}".format(username=project.user.username, domain=project.domain)
    volumes = {dist_folder: {'bind': '/usr/share/nginx/html', "mode": "ro"}}
    environment = {"VIRTUAL_HOST": "{subdomain}.{domain}".format(subdomain=project.domain, domain="angular2cloud.com")}
    client.containers.run("a2c-angular-nginx", name=name, volumes=volumes, environment=environment, detach=True)


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
