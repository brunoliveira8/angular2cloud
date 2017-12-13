import os
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

from .storage import OverwriteStorage

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}/dist.zip'.format(instance.user.username.lower(), instance.domain.lower(), filename)

# Create your models here.
class Project(models.Model):
    APP_STATUS = (
        ('RN', 'Running'),
        ('ST', 'Stopped'),
    )
    name = models.CharField(max_length = 120, help_text = "You can choose any name for your project." )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    domain = models.SlugField(unique=True, help_text="Your domain must be unique. Your project will be available at yourdomain.angular2cloud.com")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=APP_STATUS,
        default='RN',
    )
    source = models.FileField(upload_to=user_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['zip'])],
        storage=OverwriteStorage(),
        help_text = "Upload the dist folder of your Angular project as a zip file."
    )


    def save(self, *args, **kwargs):
        self.domain = self.domain.lower()
        super(Project, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('project-update', kwargs={'slug': self.domain})

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return "{user}_{domain}".format(user=self.user, domain=self.domain)