from django import forms
from django.contrib.auth.models import User
from django.template.defaultfilters import default_if_none
from wrkout.models import UserProfile, Set, Exercise, Workout
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('ProfilePicture',)

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ('Name', 'Description', )
        
class ExerciseForm(forms.ModelForm):
    Description = forms.CharField(widget=forms.Textarea())
    Difficulty = forms.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = Exercise
        fields = ('Name', 'Difficulty', 'Description', 'DemoImage', 'DemoVideo')
        
class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ('ExerciseID', 'NoOfReps', )
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
