# Direct incoming urls to views

from django.urls import path
from wrkout import views

app_name = 'wrkout'

urlpatterns = [
    path('test/', views.test_view, name='test'),
    path('test2/', views.test_view, name='test2'),
]