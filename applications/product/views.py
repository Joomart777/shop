from django.db.models import Q
from django.shortcuts import render

# Create your views here.
# Напишем CRUD для отображения
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from applications.product.filters import ProductFilter
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
    # permission_classes = [
    #     IsAuthenticatedOrReadOnly]  # Для изменения треб Аутентификац, для чтения нет ReadOnly # IsAdminUser - только для Админа # Позволяет показывать, только залогининым юзерам, аутентификац
    # pagination_class = None   # нет ограничения по кол-ву эл-в на странице по Пагинации

    pagination_class = LargeResultsSetPagination  # Прикрепил Пагинацию класс

    # filter_backends = [DjangoFilterBackend]   # Убрали ЛОкально
    # filterset_fields = ['category','owner']
    # filterset_class = ProductFilter # через filters, отдельным классомsdfsdf


    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['category', 'price']
    # search_fields = ['name','description']
    ordering_fields = ['id']  # в адресной строке ?ordering=1, ?ordering=-id (в обратном порядке, по убыванию)

    def get_queryset(self):  # Как выглядело бы без  добавленных выше библиотек и методов -- Search
        queryset = super().get_queryset()
        # print(queryset)
        search = self.request.query_params.get('search')  # params == список параметров после '?' в адресной строке, найти search
        # print(search)

        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))  # OR

        return queryset



class DeleteUpdateRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthor]   #[IsAdmin]  #Прикрепили разрешения по permissions
