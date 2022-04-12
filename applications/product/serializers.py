
from rest_framework import serializers

from applications.product.models import Product, Image, Rating


class ProductImageSerializers(serializers.ModelSerializer):    # сериализатор для обработки картинок
    class Meta:
        model = Image
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')         #owner - переопределяем это поле при входе, только для чтения. Не заполняем
    images = ProductImageSerializers(many=True, read_only=True)

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ('id', 'owner','name','description','category','price','images')

    def create(self, validated_data):       # переопределили, сохраняет вконце все что мы сделали
        request = self.context.get('request')       # context - сохран данные что передавали, вытаскиваем request
        images_data = request.FILES         # вытаскиваем все файлы из реквеста
        product = Product.objects.create(**validated_data)      ## Сохраним данные по запросу, без КАртинки.
        for image in images_data.getlist('images'):
            Image.objects.create(product=product, image=image)      # ОТ количества файлов прикрепленных, создадим лист полей, с указанием файлов, Можем соххранять несколько картин
        return product


class RatingSerializers(serializers.ModelSerializer):
    # owner = serializers.EmailField(required=False)

    class Meta:
        model = Rating
        # fields = '__all__'
        fields = ('rating',)