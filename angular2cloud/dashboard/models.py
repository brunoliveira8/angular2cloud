from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

# Create your models here.
class Project(models.Model):
    APP_STATUS = (
        ('RN', 'Running'),
        ('ST', 'Stopped'),
    )
    name = models.CharField(max_length = 120)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    domain = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=APP_STATUS,
        default='RN',
    )
    source = models.FileField(upload_to=user_directory_path)