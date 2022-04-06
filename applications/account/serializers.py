import email

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from applications.account.send_mail import send_confirmation_email

User = get_user_model()


# Импортнули класс встроенный, для работы с текущим активным кастомным юзером

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6, write_only=True, required=True)

    # При регстрации 2й пароль для сравнения и подтвеждения, не сохран-ся 2й.

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        # print(attrs)
        # в attrs идут все данные, которые мы задали в филдах при запололнении юзера. данные сохраняются в валидэйт, сравнение паролей и лишнее удалить 2й пароль

        password = attrs.get('password')
        password2 = attrs.pop('password2')

        if password != password2:
            raise serializers.ValidationError('Password is not match!!')
        return attrs

    def validate_email(self, email):
        if not email.endswith("gmail.com"):
            raise serializers.ValidationError("Your email must end with 'gmail.com'")
        return email

    def create(self, validated_data):
        # создается юзер после валидации
        user = User.objects.create_user(**validated_data)
        code = user.activation_code
        send_confirmation_email(code, user)  # send mail
        return user


class LoginSerializer(serializers.Serializer):  # Login и проверка, логин, пароль не сохраняетс в БД, сравнение пароля
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    # это как Where в postgresql
    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не Зарегистриорован!')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Неверный Пароль или Email')
            attrs['user'] = user  # сохранить юзера
            return attrs  # возвращает токен


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=6)
    password_confirm = serializers.CharField(required=True, min_length=6)

    def validate_old_password(self, old_pass):
        user = self.context.get('request').user  # Узнать какй юзер пытается поменять пароль, вытащить из request юзера
        if not user.check_password(old_pass):  # Чекаем методом в Джанго, на правильный пароль.
            raise serializers.ValidationError('Неверный Пароль!')
        return old_pass # возвратили старый пароль
    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.get('password_confirm')

        if pass1!=pass2:
            return serializers.ValidationError('Пароли не Совпадают!')
        return  attrs  # должны возвратить атрибуты обратно, проверили и возвратили
    def set_user_password(self):
        user = self.context.get('request').user
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()  # сохраняем новый пароль в БД - Хэш пароль- ч/з шифрование, данные юзера

# Можно далее написать и восстановление пароля... (самостоятельно)
# При отправке на GIT -- надо учесть, чтоб не отправили данные от Емейла, свои smtp данные пароли..для этого есть спец библиотека: python-decouple