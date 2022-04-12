from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q
from django.shortcuts import render

# Create your views here.
# Напишем CRUD для отображения
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import *
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, \
    UpdateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet

from applications.product.filters import ProductFilter
from applications.product.models import *
from applications.product.permissions import IsAdmin, IsAuthor
from applications.product.serializers import ProductSerializer, RatingSerializers


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 3  # Задали Локально, ограничение по кол-ву эл-тов на страницу
    page_size_query_param = 'page_size'
    max_page_size = 100


"""
# week12, 11/04 : закоментир, для темы декоратора ViewSet

class ListCreateView(ListCreateAPIView):         # наши Ф-ции можем навешать декораторы APIView, для GET, POSt запросов 
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [
    #     IsAuthenticatedOrReadOnly]         # Для изменения треб Аутентификац, для чтения нет ReadOnly # IsAdminUser - только для Админа # Позволяет показывать, только залогининым юзерам, аутентификац
    # pagination_class = None            # нет ограничения по кол-ву эл-в на странице по Пагинации

    pagination_class = LargeResultsSetPagination         # Прикрепил Пагинацию класс

    # filter_backends = [DjangoFilterBackend]            # Убрали ЛОкально
    # filterset_fields = ['category','owner']
    # filterset_class = ProductFilter       # через filters, отдельным классомsdfsdf


    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['category', 'price']
    # search_fields = ['name','description']
    ordering_fields = ['id']            # в адресной строке ?ordering=1, ?ordering=-id (в обратном порядке, по убыванию)

    def get_queryset(self):             # Как выглядело бы без  добавленных выше библиотек и методов -- Search
        queryset = super().get_queryset()
        # print(queryset)
        search = self.request.query_params.get('search')            # params == список параметров после '?' в адресной строке, найти search
        # print(search)

        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))  # OR

        return queryset



class DeleteUpdateRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthor]   #[IsAdmin]  #Прикрепили разрешения по permissions

"""

# ViewSet >>>
# est 3 vida ViewSet/



## Рассмотрим ModelViewSet

# class ProductViewSet(ModelViewSet):
#     queryset = Product.objects.all()       ## Queryset -- набор данных с БД
#     serializer_class = ProductSerializer          ## serializer -- переводчик, повзоляет общаться с сайтом и с питоном джанго, json -- python



## Рассмотрим след класс - GenericViewSet, работает с Mixin

# class ProductViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet):       # импортируем Миксин для вывода Листинг.
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer



## Рассмотрим обычный - ViewSet, для каждого действия надо прописать отдельно.

# class ProductViewSet(ViewSet):
#     def list(self, request):
#         pass
#     def create(self):
#         pass
#     def retrieve(self):
#         pass
#     def destroy(self):
#         pass



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]           # Фильтрация, поиск фильтрация, фильтр вывода по порядку
    # filterset_fields = ['category', 'price']
    filterset_class = ProductFilter             # Подключили Класс
    ordering_feilds = ['id', 'price' ]
    search_fields = ['name','description']

    def get_permissions(self):
        print(self.action)
        if self.action in ['list','retrieve']:   # в ViewSet
            permissions = []        # разрешение - Всем доступно, если безопасный запрос
        else:
            permissions = [IsAuthenticated]
        return  [permission() for permission in permissions]       # вывод для отображения по всем permissions

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)            # Перед сохранением, сохраняй в owner юзера кто в сессии под текущм токеном


    @action(methods=['POST'], detail=True)
    # Когда в вьюжке новый метод, надо добавить в сериализатор тоже
    def rating(self, request, pk):          #...../id_prod/rating/
        serializer = RatingSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)   # проверка

        try:
            obj = Rating.objects.get(product=self.get_object(), owner=request.user)
            obj.rating = request.data['rating']         # Если найдет, то сохранит рейтинг

        except Rating.DoesNotExist:             #  Если не найдет, то создаст новый рейтинг
            obj = Rating(owner=request.user, product=self.get_object(), rating=request.data['rating'])
        obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)


