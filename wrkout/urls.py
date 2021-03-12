# Direct incoming urls to views

from django.urls import path
from wrkout import views

app_name = 'wrkout'

urlpatterns = [
    path('', views.test_view, name='home'),
    path('test/', views.test_view, name='test'),
    path('test2/', views.test_view, name='test2'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name = 'login'),
    path('workouts/', views.browse_workouts, name='workouts_popular'),
    path('workouts/browse/', views.browse_workouts, name='exercises_popular'),
    #path('workouts/browse/popular/', views.browse_workouts, name='exercises_popular'),
    #path('workouts/browse/new/', views.browse_workouts, name='exercises_new'),
    path('workouts/create/', views.create_workout, name='create_workout'),
    #path('workouts/<workout_name>/', views.show_workout, name='show_workout'),
    
    #('exercises/', views.browse_exercises, name='exercises_popular'),
    #path('exercises/browse/', views.browse_exercises, name='exercises_popular'),
    #path('exercises/browse/popular/', views.browse_exercises, name='exercises_popular'),
    #path('exercises/browse/new/', views.browse_exercises, name='exercises_new'),
    path('exercises/create/', views.create_exercise, name='create_exercise'),
    #path('exercises/<exercise_name>/', views.show_exercise, name='show_exercises')
    
    #path('users/', views.show_profile, name='show'),
    #path('users/edit/', views.edit_profile, name='edit'),
    #path('users/<username>/, views.show_profile, name='show'),
    
    
    # I commented some of the paths out, because their views dont exist yet, so
                                                    # the server would not run.
   
]