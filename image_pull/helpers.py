import os
import uuid
import requests

from django.core.files.uploadedfile import UploadedFile
from rest_framework.response import Response
from rest_framework import status

from image_pull.models import Image
from sap_project.settings import MEDIA_ROOT
from sap_project import logger

def download_file(url:str, local_file_path:str) -> (str, bool):
    raw_data = requests.get(url)
    data = raw_data.content
    content_length = raw_data.headers.get('content-length')
    content_type = raw_data.headers.get('content-type')
    if not content_length or not content_type:
        logger.error(f"Missing content length or content type headers for {url}")
        return "", False
    
    format = content_length.split("/")[-1]

    file_name = os.path.join(local_file_path, f'{str(uuid.uuid4())}.{format}')
    with open(file_name, 'wb') as fp:
        fp.write(data)
    logger.info(f"File downloaded from {url} and saved as {file_name}")
    return file_name, True

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
            logger.info(f"Image data saved for {url}")
        image_instaces.append(image_object)
    return image_instaces

def list_valid_images() -> list:
    return Image.objects.filter(is_valid = True)

def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(e)
            return Response("something went wrong", status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # Or raise a custom exception, or handle it in another way

    return wrapper
