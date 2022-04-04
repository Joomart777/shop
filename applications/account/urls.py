from django.urls import path

from applications.account.views import RegisterApiView

urlpatterns = [
    path('register/', RegisterApiView.as_view())
]