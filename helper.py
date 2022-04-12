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


*******>>>> PART2 (account)

пишем классы в моделс аккаунт

переход CTRL + mouse --> AbstractModel -- > coppy --> correct in account/models add class UserManager, create_user -->  is_superuser -False (обычный юзер создается)

добавить в settings:

AUTH_USER_MODEL = 'account.CustomUser' 

drop shop_db;

create db shop_db; --> создать заново, с переопределенным новым ююзером

migrate

createsuperuser --> теперь по емейлу создается, после переопределения 
runserver --> вход в админку --> ТЕперь подтверждение входа через email: admin@admin.com 

чтоб появился юзер в браузер --> register in admin:
admin.site.register(CustomUser)

urls

post menyaem

Пишем валидацию def validate in serializers

--> GIT
git add .
git commit...
git push origin master


****>>>>
зайт в gmail acc --> управл аккаунтом-- безопасность -- ненадеж приложения -- активировать разрешено (инче не сработает отсылка в локалхост)

--> send_mail.py (добавить свою почту -- настроить smtp,  как отправщик, для отправки почты, пользоваться сервисом емейла)

--> settings -- добавить смтп запрос почты для своего емейла
-- удалить старое свое, иначе похожий не создаст
--> Postman -- добавить пост зарегить нового со своей почтой

--> Напишем активацию юзера, при нажатии на ссылку в почте. статус Is Active
urls (path uuid (hash code))--> view (ActivationView)
Теперь активация Успешна - В Джанго фрейм проводит активацию

-->>> НАСТРОИМ АУТЕНТИФИКАЦИЮ --логика идентификации пользователя, для работы только со своими данными.
TOKEN -- для доступа к своим данным у каждого логина позволяет Токены -- набор цифр и букв, для подтверждения логина. Используем встроенный токен Джанго.
Добавить в Installed Apps -- authtoken , Также добавить REst_Framework = {} (ниже отдельно)

--> Сделаем, чтоб продукты смотрел свой создатель и владелец, аутентификация:
product/view: permission_classes = [IsAuthenticated] 

--> account/views: пишем логинизацию
class LoginApiView(..)
-->acc/urls/login: path('login/', LoginApiView.as_view()),

--> serializers: пишем LoginSerializer  -- проверка и присвоение токена на верный логин

--> Postman--> POST--> acc/login --> token  (После логина дается каждому токен на сессию, и с этим токеном работает со своими данными), есть и другие виды токенов, которые меняются по тайму по настройке, в Джанго встроенн на сессию.
-->Postman --> Headers-->(GET) authorization (with token: Token 1a37516898be44609ab2e403ddff4b35565d579e)

--> Пишем ЛОгаут
--> logout -- delete --> path

--> Postman -- check logout (with token)

--> Каждый вход со своим токеном, для всех юзеров


*********>>>>> 
--> Создадим change password

acc/view-- class changepassw
serializers -- change pass
urls

--> Postman --> POST --> Login--> token --> Headers --> Body --> проверим
olp_passw ..
password ...
passwrord_confirm ... OK

БИблиотеки для сокрытия данных своих пароли smtp и тд от емейла:
python-decouple
dj-config-url

touch .env
--env:
SECRET_KEY = 'django-insecure-41aa_h2kedbp%0@!mkw!#ji(g_mccp$*0%o1v#7l)i504)%lvt'
DEBUG = True

скопировать с settings и поменять:
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',') 


и добавить в .env:
SECRET_KEY = 'django-insecure-41aa_h2kedbp%0@!mkw!#ji(g_mccp$*0%o1v#7l)i504)%lvt'
DEBUG = True
ALLOWED_HOSTS=localhost, 127.0.0.1



сокрыть БД (все настройки скроет в одну строчку)
DATABASES = {
'default': dj_database_url.config(
    default=config('DATABASE_URL')
)
}

--> .env:
DATABASE_URL = 'postgresql://joomart:1@localhost:5432/shop_db'
/// удалить лишние пробелы, до и после =


... добавить данные smtp из settings

--> далее поменять данные в settings для smtp сделать ссылку на config 
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')


--> Отправляем на GIT --> 
git add .
git commit -m 'added .env'
push origin master

в Репозиториях нет конфиденц данных наших -- нет папки .env

git log -- Посмотреть историю по отправленным git

Вернуть предыдущ версию из Гита:
git reset 'название комита'
git push origin master

******>>>> swagger
--> import swagger lib
http://localhost:8000/swagger/ -- для просмотра всех url 

--> setings -- rest_framework
--> views -- отмена глобальной пагинации -- отмен огранич по кол-ву эл-в по пагинации на стр

--> Postman -- http://localhost:8000/product/?page=2 -- просмотр на 2й стр

--> добавим класс для пагинаций, котор можно навешать на любую пагинацию др страниц:
pagination_class = LargeResultsSetPagination 


******>>>>> 
Теория - возможно будут спрашивать в интервью:

MVC -- model view controller (controller -- маршрутизаторы)
MVT -- model view templates (шаблоны, джанго в основном работает на шаблонах)

DRF - Django Rest Framework  -- бекэнд  чистый 

Rest - Representation State (Правило кода по фреймфорку)

DT - Django Templates (шаблонный Джанго) - самостоятельно







