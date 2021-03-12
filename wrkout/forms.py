from django import forms
from django.contrib.auth.models import User
from wrkout.models import UserProfile, Set, Exercise, Workout

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('ID', 'picture',)

class WorkoutForms(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ('ID', 'name', 'description', )
        
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('ID', 'name', 'difficulty', 'description', )
        
class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ('ExerciseID', 'No. of reps', )
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
