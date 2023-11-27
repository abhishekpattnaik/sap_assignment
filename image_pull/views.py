from rest_framework import status, request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from image_pull.models import Image
from image_pull.helpers import save_images_data, list_valid_images
from image_pull.serializers import ImageSerializer

class ImageAPIView(APIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        if pk is not None:
            data =  Image.objects.get(pk=pk)
            serializer = ImageSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        image_instances = list_valid_images()
        serializer = ImageSerializer(image_instances, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: request, format=None):
        image_instances = save_images_data(request)
        serializer = ImageSerializer(image_instances, many = True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
