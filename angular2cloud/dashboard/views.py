import docker

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required

from .models import Project
from .utils import start_container, stop_container

# Create your views here.
def index(request):
    return redirect('project-list')


class ProjectList(ListView):
    context_object_name = 'projects'
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class ProjectCreate(CreateView):
    model = Project
    fields = ['name', 'domain', 'source']

    def form_valid(self, form):
        n_projects = len(Project.objects.filter(user=self.request.user))
        if n_projects == 2:
            form.add_error(None, "You can create at most 2 projects")
            return super().form_invalid(form)
        form.instance.user = self.request.user
        return super().form_valid(form)


class ProjectUpdate(UpdateView):
    context_object_name = 'project'
    slug_field = 'domain'
    template_name_suffix = '_update_form'
    fields = ['source']
    model = Project
    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class ProjectDelete(DeleteView):
    model = Project
    context_object_name = 'project'
    slug_field = 'domain'
    success_url = reverse_lazy('project-list')


class ProjectActivate(View):
    def post(self, request):
        slug = request.POST['slug']
        project = get_object_or_404(Project, user=request.user, domain=slug)
        if project.status == 'RN':
            stop_container(project)
            project.status = 'ST'
            project.save(update_fields=['status'])
        else:
            start_container(project)
            project.status = 'RN'
            project.save(update_fields=['status'])
        return redirect('project-update', slug=slug)