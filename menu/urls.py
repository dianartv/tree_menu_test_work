from django.urls import path

from .views import my_view, Page

app_name = 'pages'

urlpatterns = [
    path('', Page.as_view(), name='page'),
    path('<str:url_type>/', my_view, name='url'),
]
