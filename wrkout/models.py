from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    SavedWorkouts = models.ManyToManyField('Workout', related_name='%(class)s_requests_created')
    LikedWorkouts = models.ManyToManyField('Workout')
    LikedExercises = models.ManyToManyField('Exercise')
    Username = models.CharField(max_length=30)
    Password = models.CharField(max_length=30)
    ProfilePicture = models.ImageField(upload_to='profile_images', blank=True)

class Exercise(models.Model):
    ExerciseID = models.AutoField(primary_key=True)
    CreatorID = models.ForeignKey(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=30)
    Description = models.CharField(max_length=500)
    Difficulty = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    DemoImage = models.ImageField(upload_to='exercise_images', blank=True)
    DemoVideo = models.URLField(blank=True)
    Date = models.DateField()
    Likes = models.IntegerField(default=0)
    
    

class Workout(models.Model):
    WorkoutID = models.AutoField(primary_key=True)
    CreatorID = models.ForeignKey(User, on_delete=models.CASCADE)
    Sets = models.ManyToManyField('Set')
    Name = models.CharField(max_length=30)
    Description = models.CharField(max_length=500)
    Date = models.DateField()
    Likes = models.IntegerField(default=0)

class Set(models.Model):
    SetID = models.AutoField(primary_key=True)
    ExerciseID = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    NoOfReps = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    
