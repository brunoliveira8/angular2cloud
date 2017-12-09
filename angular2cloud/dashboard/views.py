from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Project

# Create your views here.
def index(request):
    return render(request, 'dashboard/index.html')

class ProjectCreate(CreateView):
    model = Project
    fields = ['name', 'domain', 'source']
    success_url = "/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)