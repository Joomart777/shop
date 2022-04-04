from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.account.serializers import RegisterSerializer


class RegisterApiView(APIView):
    #POST - переопределяем методо пост, отработает для post
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = 'Vy uspeshno ZAREGILIS. Vam otpravlen email s Aktivaciey'
            return Response(message, status=201)
        return Response(status=status.HTTP400_BAD_REQUEST)