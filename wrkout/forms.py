from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from django.http import request
from django.template.defaultfilters import default_if_none
from wrkout.models import UserProfile, Set, Exercise, Workout
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('ProfilePicture',)
        labels = {
            'ProfilePicture': 'Profile picture'
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('ProfilePicture',)
        labels = {
            'ProfilePicture': 'New profile picture',
        }
        help_texts = {
            'ProfilePicture': 'Leave blank to remain unchanged'
        }

class WorkoutForm(forms.ModelForm):
    Description = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Workout
        fields = ('Name', 'Description', )
        
class ExerciseForm(forms.ModelForm):
    Description = forms.CharField(widget=forms.Textarea())
    Difficulty = forms.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = Exercise
        fields = ('Name', 'Difficulty', 'Description', 'DemoImage', 'DemoVideo')
        labels = {
            'DemoImage': 'Demonstration image',
            'DemoVideo': 'Demonstration video',
        }
        help_texts = {
            'DemoVideo': 'Optional, but must be from youtube.com if used'
        }
        
class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ('ExerciseID', 'NoOfReps', )
        
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class EditUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['email'].required = False
        self.fields['password'].required = False

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        labels = {
            'username': 'New username',
            'email': 'New email',
            'password': 'New password',
        }
        help_texts = {
            'username': 'Leave blank to remain unchanged',
            'email': 'Leave blank to remain unchanged',
            'password': 'Leave blank to remain unchanged',
        }
        widgets = {
            'password': forms.PasswordInput()
        }
