from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status, request
from rest_framework.views import APIView
from rest_framework.response import Response

from image_pull.models import Image
from image_pull.helpers import save_images_data, list_valid_images
from image_pull.serializers import UserSerializer, GroupSerializer, ImageSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Image.objects.filter(is_valid = True)
    serializer_class = ImageSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ImageAPIView(APIView):
    def get(self):
        image_instances = list_valid_images()
        serializer = ImageSerializer(image_instances, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, pk):
        data =  Image.objects.get(pk=pk)
        serializer = ImageSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: request, format=None):
        image_instances = save_images_data(request)
        serializer = ImageSerializer(image_instances, many = True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
