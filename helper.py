touch requirements.txt
pip install -r requirements.txt
django-admin startproject shop .
 ./manage.py makemigrations
mkdir applications  (Все аккаунты, пароли и тд будут в этой папке, лучше так в одну папку всех)
cd applications/

../manage.py startapp product (вызвать с выше папки и создать приложение)
../manage.py startapp account

cd ..

 ./manage.py runserver
You have 18 unapplied migration(s). -- c settings (главный)-- сообщает о не добавленных --> надо добавить в databases, applications данные.

Сначала создать БД:
create database shop_db;

Settings: 
databases---  'ENGINE': 'django.db.backends.postgresql',

   'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shop_db',
        'USER': 'joomart',
        'PASSWORD' : '1',
        'HOST' : 'localhost',
        'PORT' : 5432,  (порт postgresql)
        

 ./manage.py migrate

добавим классы в product/models:
class Category(models.Model):
    slug = models.SlugField(max_length=30, primary_key=True) -- Primary Key - не будет создаваться при True. Будем идентифицировать просто по полю Slug - уникальное название
    description = models.TextField(blank=True, null=True)

Чтобы добавить в БД, надо в settings (main):
INSTALLED_APPS = [
  #Apps
    'applications.product',  (applications --- означает выше папку, где хранятся все приложения)
    'applications.account',

Также добавить в name product/apps:
name = 'applications.product'

 ./manage.py makemigrations
    - Create model Category

./manage.py migrate

./manage.py createsuperuser  --- создать админа, иначе в БД никого нет. Суперюзер - все привилегии неограниченно. Админ


models -- наши модели,  наши таблицы в БД, которые Джанго отсылает orm 
views --наши представления в браузере
urls -- наши адресы для отображения
serializers -- питан джанго сериалайзер
admin -- регистрируем админку на сайт только отображает но ничего не делает

-->product/models:  (для отображения)
    def __str__(self):
        return self.slug


User = get_user_model() # переопределим встроенную ф-ю по юзерам

class Product(models.Model):
    owner = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE) -- переопределим юзера, связанно сверху вначале как определили, 
    name = models.CharField(max_length=30, ) -- обязат условие длину задать, иначе ОШИБКА
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)) -- обязат условие МАКС после запятой, округление
    category = models.ForeignKey(Category,related_name='product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', null=True, blank=True) --- загрузить в папку images


requirements.txt:
добавить  
pillow  (библ по картинкам)


---> Любые изменения с  полями (моделс) -- надо делать Миграцию после. Чтоб добавились изменения в БД


-->admins:
admin.site.register(Product)   --- регистрируем продукт, чтоб отображался в браузер

--> settings(main):
MEDIA_ROOT = BASE_DIR/'media/'  -- так разделять медиа файлы в отдельной папке Медиа


--> views:
class ListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()  -- запросы
    serializer_class = ProductSerializer  -- переводчик с JSON сериалайзер
    
--> create>> serializers:
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        

---> создать urls:
urlpatterns = [
    path('', ListCreateView.as_view()),  -- если пустой отобразить все
]

--> main urls:
    path('product/', include('applications.product.urls')) -- импорт с django.urls
    
---> settings:
обязательно добавить в INSTALLED APPS:
    #modules
    'rest_framework'
    
---> браузер проверка -- отображает

---> Postman:
GET - получать список
POST - создать список

--> views:
class DeleteUpdateRetrieveView(RetrieveUpdateDestroyAPIView):  (можно так объединить все 3 метода, поскольку похожие по запросу по айдишке (удал, изме, детально)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
---> second urls:
    path('<int:pk/>', DeleteUpdateRetrieveView.as_view()),
    
    
---> GITHUB -- и все ОК

touch .gitignore
git init
git add .
 git commit -m 'add product model and CRUD'
git remote add origin git@github.com:Joomart777/shop.git  (скопировать связь с SSH c Github)
 git push origin master

Поделиться -- с адресом Гита в Комюнити 

    

