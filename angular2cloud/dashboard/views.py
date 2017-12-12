from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Project

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

