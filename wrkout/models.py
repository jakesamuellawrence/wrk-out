from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    UserID = models.AutoField(primary_key=True, on_delete=models.CASCADE)
    SavedWorkouts = models.ManyToManyField(Workout)
    LikedWorkouts = models.ManyToManyField(Workout)
    LikedExercises = models.ManyToManyField(Exercises)
    Username = models.CharField(max_length=30)
    Password = models.CharField(max_length=30)
    ProfilePicture = models.ImageField(upload_to='profile_images', blank=True)

class Exercise(models.Model):
    ExerciseID = models.AutoField(primary_key=True, on_delete=models.CASCADE)
    CreatorID = models.ForeignKey(User)
    Name = models.CharField(max_length=30)
    Description = models.CharField(max_length=500)
    Difficulty = models.IntegerRangeField(min_value=1, max_value=5)
    DemoImage = models.ImageField(upload_to='exercise_images', blank=True)
    DemoVideo = models.URLField(blank=True)
    Date = DateField()
    Likes = IntegerField(default=0)
    
    

class Workout(models.Model):
    WorkoutID = models.AutoField(primary_key=True, on_delete=models.CASCADE)
    CreatorID = models.ForeignKey(User)
    Sets = models.ManyToManyField(Set)
    Name = models.CharField(max_length=30)
    Description = models.CharField(max_length=500)
    Date = DateField()
    Likes = IntegerField(default=0)

class Set(models.Model):
    SetID = models.AutoField(primary_key=True, on_delete=models.CASCADE)
    ExerciseID = models.ForeignKey(Exercise)
    NoOfReps = IntegerField(min_value=1)
    
    
