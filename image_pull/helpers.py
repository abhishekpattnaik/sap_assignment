import os
import uuid
import requests

from django.core.files.uploadedfile import UploadedFile

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

    for url in image_urls:
        file_name = str(uuid.uuid4())
        image_object = Image.objects.create(file_name = file_name, source_url = url)
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

# class YourModelListAPIView(APIView):
#     def get(self, request, format=None):
#         queryset = YourModel.objects.all()
#         serializer = YourModelSerializer(queryset, many=True)
#         return Response(serializer.data)

# class YourModelDetailAPIView(APIView):
#     def get_object(self, pk):
#         try:
#             return YourModel.objects.get(pk=pk)
#         except YourModel.DoesNotExist:
#             return None

#     def get(self, request, pk, format=None):
#         instance = self.get_object(pk)
#         if instance is not None:
#             serializer = YourModelSerializer(instance)
#             return Response(serializer.data)
#         else:
#             return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)