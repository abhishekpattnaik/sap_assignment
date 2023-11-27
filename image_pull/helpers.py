import os
import uuid
import requests

from django.core.files.uploadedfile import UploadedFile
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


from image_pull.models import Image
from sap_project.settings import MEDIA_ROOT


def download_file(url:str, local_file_path:str) -> (str, bool):
    try:
        raw_data = requests.get(url)
        data = raw_data.content
        raw_data.headers['content-length']
        content_length = raw_data.headers['content-type']
        format = content_length.split("/")[-1]

        file_name = os.path.join(local_file_path, f'{str(uuid.uuid4())}.{format}')
        f = open(file_name,'wb') 
        f.write(data) 
        f.close()
        return file_name, True
    except KeyError as e:
        print(f"Invaid url: {url}", e)
        return "", False

def save_images_data(request) -> list:
    image_urls = request.data.get('source_url', [])
    locale_file_path = os.path.join(MEDIA_ROOT, 'images')
    image_instaces = []
    user = request.user

    for url in image_urls:
        file_name = str(uuid.uuid4())
        image_object = Image.objects.create(file_name = file_name, source_url = url, user = user)
        local_file_path, is_valid = download_file(image_object.source_url, locale_file_path)

        if is_valid:
            image_object.is_valid = True
            image_object.image = UploadedFile(file=open(local_file_path, "rb"))
            image_object.local_file_path = local_file_path
            image_object.save()
            os.remove(local_file_path)
        image_instaces.append(image_object)
    return image_instaces

def list_valid_images() -> list:
    return Image.objects.filter(is_valid = True)
