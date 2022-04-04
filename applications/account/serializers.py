from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()
# Импортнули класс встроенный, для работы с текущим юзером

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6, write_only=True, required=True)
    # При регстрации 2й пароль для сравнения и подтвеждения, не сохран-ся 2й.

    class Meta:
        model = User
        fields = ('email','password','password2')

    def validate(self, attrs):
        # print(attrs)
        # данные сохраняются в валидэйт, сравнение паролей и лишнее удалить 2й пароль

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
        #создается юзер после валидации
        user = User.objects.create_user(**validated_data)
        code = user.activation_code
        # send mail
        # TODO: Send mail

        return user