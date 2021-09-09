from rest_framework import serializers
from .models import Client, Product, Bill


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Client


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Product


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Bill


class UploadSerializer(serializers.Serializer):
    file_uploaded = serializers.FileField()

    class Meta:
        fields = ['file_uploaded']