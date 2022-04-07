from django.contrib.auth import get_user_model
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.account.serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer

User = get_user_model()  # для работы с кастомным юзером


class RegisterApiView(APIView):
    # POST - переопределяем метод пост, отработает для post
    permission_classes = [AllowAny] # на регистр-ю Аутентиф не нужно, для всех
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = 'Vy uspeshno ZAREGILIS. Vam otpravlen email s Aktivaciey'
            return Response(message, status=201)
        return Response(status=status.HTTP400_BAD_REQUEST)


class ActivationView(APIView):
    def get(self, request, activation_code):  # GET zapros, принимает request, activation_code
        try:
            user = User.objects.get(
                activation_code=activation_code)  # вытащить юзера, у котор активкод = по запросу активкод
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response('Вы успешно активировали свой аккаунт', status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response('Активационный Код Недействительный', status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(ObtainAuthToken):  # Аутентификация получение ТОкена
    serializer_class = LoginSerializer  # не объект а присваивание классов


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # устанавливает право доступа, если он вошел, может и выйти

    def post(self, request):  # post zapros
        try:
            user = request.user
            Token.objects.filter(
                user=user).delete()  # Удалили ТОкен после выхода, чтоб в дальнейшем не пользовались, и не входили в доступ
            return Response('Вы Вышли, Разлогинились')
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):  # post запрос
        data = request.data  # в request хранится все данные о вошедшем юзере, выводим через data
        serializer = ChangePasswordSerializer(data=data, context={
            'request': request})  # request (определен юзера, котор работает) передали в контекст, передаем данные в виде словаря в Сериализатор
        serializer.is_valid(raise_exception=True)  # Если все ОК, вызвать метод ниже
        serializer.set_user_password()
        return Response('Пароль успешно ОБновлен!')
