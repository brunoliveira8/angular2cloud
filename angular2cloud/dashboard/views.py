from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from .models import Project

# Create your views here.
@login_required
def index(request):
    return render(request, 'dashboard/index.html')

class ProjectCreate(CreateView):
    model = Project
    fields = ['name', 'domain', 'source']
    success_url = "/"

    def form_valid(self, form):
        n_projects = len(Project.objects.filter(user=self.request.user))
        if n_projects == 2:
            form.add_error(None, "You can create at most 2 projects")
            return super().form_invalid(form)
        form.instance.user = self.request.user
        return super().form_valid(form)