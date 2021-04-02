# Direct incoming urls to views

from django.contrib.auth.models import PermissionManager
from django.urls import path
from django.views.generic.base import RedirectView
from wrkout import views

app_name = 'wrkout'

urlpatterns = [
    path('', RedirectView.as_view(permanent=True, url="workouts/browse/popular"), name='home'),
    path('test/', views.test_view, name='test'),
    path('test2/', views.test_view, name='test2'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name='logout'),
    #path(actionUrl, views.add_button, name = 'add_button'), 
    
    path('workouts/', RedirectView.as_view(permanent=True, url="browse/popular")),
    path('workouts/browse/', RedirectView.as_view(permanent=True, url="popular")),
    path('workouts/browse/popular/', views.browse_popular_workouts, name='workouts_popular'),
    path('workouts/browse/new/', views.browse_newest_workouts, name='workouts_new'),
    path('workouts/browse/difficulty/', views.browse_difficulty_workouts, name='workouts_difficulty'),
    path('workouts/create/', views.create_workout, name='create_workout'),
    path('workouts/<slug:workout_Name_Slug>/', views.show_workout, name='show_workout'),
    path('workouts/<slug:workout_Name_Slug>/save', views.save_workout, name="save_workout"),
    path('workouts/<slug:workout_Name_Slug>/unsave', views.unsave_workout, name="unsave_workout"),
    path('workouts/<slug:workout_Name_Slug>/delete', views.delete_workout, name="delete_workout"),
    path('workouts/<slug:workout_Name_Slug>/like', views.like_workout, name="like_workout"),
    path('workouts/<slug:workout_Name_Slug>/unlike', views.unlike_workout, name="unlike_workout"),
    path('workouts/<slug:workout_Name_Slug>/dislike', views.dislike_workout, name="dislike_workout"),
    path('workouts/<slug:workout_Name_Slug>/undislike', views.undislike_workout, name="undislike_workout"),
    
    path('exercises/', RedirectView.as_view(permanent=True, url="browse/popular")),
    path('exercises/browse/', RedirectView.as_view(permanent=True, url="popular")),
    path('exercises/browse/popular/', views.browse_popular_exercises, name='exercises_popular'),
    path('exercises/browse/new/', views.browse_newest_exercises, name='exercises_new'),
    path('exercises/browse/difficulty/', views.browse_difficulty_exercises, name='exercises_difficulty'),
    path('exercises/create/', views.create_exercise, name='create_exercise'),
    path('exercises/<slug:exercise_Name_Slug>/', views.show_exercise, name='show_exercise'),
    path('exercises/<slug:exercise_Name_Slug>/delete', views.delete_exercise, name='delete_exercise'),
    path('exercises/<slug:exercise_Name_Slug>/like', views.like_exercise, name="like_exercise"),
    path('exercises/<slug:exercise_Name_Slug>/unlike', views.unlike_exercise, name="unlike_exercise"),
    path('exercises/<slug:exercise_Name_Slug>/dislike', views.dislike_exercise, name="dislike_exercise"),
    path('exercises/<slug:exercise_Name_Slug>/undislike', views.undislike_exercise, name="undislike_exercise"),
    
    path('users/<slug:username>/', views.view_profile, name='profile'),
    path('users/<slug:username>/edit', views.edit_profile, name='edit_profile'),
    
    
    # I commented some of the paths out, because their views dont exist yet, so
                                                    # the server would not run.
   
]