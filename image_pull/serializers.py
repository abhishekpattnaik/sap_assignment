from rest_framework import serializers

from image_pull.models import Image

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ['local_file_path', 'file_name', 'image', 'source_url', 'is_valid']
