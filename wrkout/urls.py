# Direct incoming urls to views

from django.urls import path
from wrkout import views

urlpatterns = [
    path('test/', views.test_view, name='test'),
]