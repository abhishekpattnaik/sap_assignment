import os

from django.db import models
# from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_image_extension(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    _, file_extension = os.path.splitext(value.name)
    if file_extension.lower() not in valid_extensions:
        raise ValidationError('Invalid file extension. Supported formats: JPG, JPEG, PNG, GIF.')


class Image(models.Model):
    local_file_path = models.CharField(max_length=250, null=True, blank= True)
    file_name = models.CharField(max_length=150, unique=True)
    source_url = models.URLField(max_length=150)
    image = models.ImageField(upload_to='images/', validators=[validate_image_extension], null=True, blank= True)
    is_valid = models.BooleanField(default=False)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    # def save(self, *args, **kwargs):
    #     self.local_file_path = os.path.join(MEDIA_ROOT, 'images')
    #     local_file_path = download_file(self.source_url, self.local_file_path)
    #     self.image = UploadedFile(file=open(local_file_path, "rb"))
    #     super(Image, self).save(*args, **kwargs)
    #     os.remove(local_file_path)

    def __str__(self):
        return self.file_name
