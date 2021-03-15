from django import forms
from django.contrib.auth.models import User
from wrkout.models import UserProfile, Set, Exercise, Workout

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('ProfilePicture',)

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ('Name', 'Description', )
        
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('Name', 'Difficulty', 'Description', )
        
class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ('ExerciseID', 'NoOfReps', )
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
