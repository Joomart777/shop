from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.product.views import *

router = DefaultRouter()  ## Router -- маршрутизаторы, направляет дальнейшие действия, встроено CRUD
router.register('', ProductViewSet) # регистрируем маршутизаторы, путь тот же ''


urlpatterns = [
    # path('', ListCreateView.as_view()),
    # path('<int:pk>/', DeleteUpdateRetrieveView.as_view()),
    # path('', ProductViewSet.as_view({'get':'list'})),   ## -- ViewSet, as_view. если будет запрос Get --> выведи list. В отличии от ApiView (где отдельно для каждого метод)

    path('', include(router.urls)),  # регистрир Маршрутизатор.
]