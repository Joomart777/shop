from django.shortcuts import render

# Create your views here.
# Напишем CRUD для отображения
from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from applications.product.models import *
from applications.product.permissions import IsAdmin, IsAuthor
from applications.product.serializers import ProductSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3  # Задали Локально, ограничение по кол-ву эл-тов на страницу
    page_size_query_param = 'page_size'
    max_page_size = 100


class ListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly]  # Для изменения треб Аутентификац, для чтения нет ReadOnly # IsAdminUser - только для Админа # Позволяет показывать, только залогининым юзерам, аутентификац
    # pagination_class = None   # нет ограничения по кол-ву эл-в на странице по Пагинации

    pagination_class = LargeResultsSetPagination  # Прикрепили Пагинацию класс


class DeleteUpdateRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthor]   #[IsAdmin]  #Прикрепили разрешения по permissions
