from django.shortcuts import render

# Create your views here.
# Напишем CRUD для отображения
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated

from applications.product.models import *
from applications.product.serializers import ProductSerializer


class ListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Позволяет показывать, только залогининым юзерам, аутентификац

class DeleteUpdateRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
