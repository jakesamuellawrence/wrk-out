from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify

class UserProfile(models.Model):
    UserAccount = models.OneToOneField(User, on_delete=models.CASCADE)
    
    UserID = models.AutoField(primary_key=True)
    Slug = models.SlugField(unique=True, null=True)
    SavedWorkouts = models.ManyToManyField('Workout', related_name='%(class)sSaved')
    LikedWorkouts = models.ManyToManyField('Workout')
    LikedExercises = models.ManyToManyField('Exercise')
    ProfilePicture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.UserAccount.username

    def save(self, *args, **kwargs):
        self.Slug = slugify(self.UserAccount.username)
        super(UserProfile, self).save(*args, **kwargs)

class Exercise(models.Model):
    ExerciseID = models.AutoField(primary_key=True)
    CreatorID = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    Slug = models.SlugField(unique=True, null=True)
    Name = models.CharField(max_length=30)
    Description = models.CharField(max_length=500)
    Difficulty = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    DemoImage = models.ImageField(upload_to='exercise_images', blank=True)
    DemoVideo = models.URLField(blank=True)
    Date = models.DateField()
    Likes = models.IntegerField(default=0)

    def __str__(self):
        return self.Name

    def save(self, *args, **kwargs):
        self.Slug = slugify(self.Name)
        super(Exercise, self).save(*args, **kwargs)


    
    

class Workout(models.Model):
    WorkoutID = models.AutoField(primary_key=True)
    CreatorID = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    Slug = models.SlugField(unique=True, null=True)
    Sets = models.ManyToManyField('Set')
    Name = models.CharField(max_length=30)
    Description = models.CharField(max_length=500)
    Difficulty = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=0)
    Date = models.DateField()
    Likes = models.IntegerField(default=0)

    def __str__(self):
        return self.Name

    def save(self, *args, **kwargs):
        self.Slug = slugify(self.Name)
        super(Workout, self).save(*args, **kwargs)



class Set(models.Model):
    SetID = models.AutoField(primary_key=True)
    ExerciseID = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    NoOfReps = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    
    
