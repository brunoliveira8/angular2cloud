from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

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
        default='ST ',
    )
    source = models.FileField(upload_to=user_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['zip'])],
        help_text = "Upload the dist folder of your Angular project as a zip file."
    )

