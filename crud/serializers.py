from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    images_list = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_images_list(self,instance):
        try:
            data = ImagesSerializer(instance.product_images.all(),many=True).data if instance.product_images else None
        except Exception as e:
            print(e)
            data = []
        return data



class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'