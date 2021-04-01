from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from wrkout.models import User, Exercise, Workout,Set, UserProfile
from wrkout.forms import UserForm, ExerciseForm, WorkoutForm, UserProfileForm, EditUserForm, EditProfileForm
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
import math

# Create your views here.

def test_view(request):
    return render(request, 'wrkout/view_exercise.html', {
        'result': Workout.objects.first(), 
        'is_owner': True})

def search(request):
    if request.method == 'GET':
        context_dict = {}  
        query =  request.GET.get('search-key')
        if query:
            try:
                exercises =  Exercise.objects.filter(Name__icontains=query)
                workouts = Workout.objects.filter(Name__icontains=query)
                results = [exercise for exercise in exercises] + [workout for workout in workouts]
                context_dict['results'] = results
            except Exercise.DoesNotExist and Workout.DoesNotExist:
                context = None
            return render(request,'wrkout/browse.html',context=context_dict)
        else:
            return render(request,'wrkout/browse.html',{})
    else:
        return render(request,'wrkout/browse.html',{})
 
def show_workout(request, workout_Name_Slug):
    context_dict = {}

    try:
        workout = Workout.objects.get(Slug=workout_Name_Slug)
        context_dict['result'] = workout
        
    except Workout.DoesNotExist:
        return render(request, 'wrkout/missing_page.html')

    return render(request, 'wrkout/view_workout.html', context_dict)
  
def show_exercise(request, exercise_Name_Slug):
    context_dict = {}

    try:
        exercise = Exercise.objects.get(Slug=exercise_Name_Slug)
        context_dict['result'] = exercise
        
    except Exercise.DoesNotExist:
        return render(request, 'wrkout/missing_page.html')

    return render(request, 'wrkout/view_exercise.html', context=context_dict)
    
def browse_popular_workouts(request):
    workout_list = Workout.objects.order_by('-Likes')
    context_dict = {}
    context_dict['results'] = workout_list
    response = render(request, 'wrkout/browse.html', context=context_dict)
    return response
    
def browse_popular_exercises(request):
    exercise_list = Exercise.objects.order_by('-Likes')
    context_dict = {}
    context_dict['results'] = exercise_list
    response = render(request, 'wrkout/browse.html', context=context_dict)
    return response
    
def browse_newest_workouts(request):
    workout_list = Workout.objects.order_by('-Date')
    context_dict = {}
    context_dict['results'] = workout_list
    response = render(request, 'wrkout/browse.html', context=context_dict)
    return response
    
def browse_newest_exercises(request):
    exercise_list = Exercise.objects.order_by('-Date')
    context_dict = {}
    context_dict['results'] = exercise_list
    response = render(request, 'wrkout/browse.html', context=context_dict)
    return response
    
def browse_difficulty_workouts(request):
    workout_list = Workout.objects.order_by('-Difficulty')
    context_dict = {}
    context_dict['results'] = workout_list
    response = render(request, 'wrkout/browse.html', context=context_dict)
    return response
    
def browse_difficulty_exercises(request):
    exercise_list = Exercise.objects.order_by('-Difficulty')
    context_dict = {}
    context_dict['results'] = exercise_list
    response = render(request, 'wrkout/browse.html', context=context_dict)
    return response

def view_profile(request,username):
    try:
        profile = UserProfile.objects.get(Slug=username)
    except UserProfile.DoesNotExist:
        return render(request, 'wrkout/missing_page.html')
    context_dict = {}
    try:
        workouts = Workout.objects.filter(CreatorID=profile)
        exercises = Exercise.objects.filter(CreatorID=profile)
    except Workout.DoesNotExist:
        workouts = None
    except Exercise.DoesNotExist:
        exercises = None

    context_dict = {'profile': profile,'created_workouts': workouts,'created_exercises':exercises,}
    return render(request, 'wrkout/view_profile.html', context_dict)
    
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.UserAccount = user

            if 'ProfilePicture' in request.FILES:
                profile.ProfilePicture = request.FILES['ProfilePicture']
            profile.save()

            return render(request, 'wrkout/login.html', {'just_registered': True})
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'wrkout/register.html',context = {'user_form': user_form,'profile_form': profile_form,})
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                next_href = request.GET.get('next', reverse('wrkout:home'))
                return redirect(next_href)
            else:
                return render(request, 'wrkout/login.html', {'error': "Your Wrkout account is disabled."})
        else:
            print(f"Invalid login details: {username}, {password}")
            return render(request, 'wrkout/login.html', {'error': "Invalid login details supplied."})
    else:
        return render(request, 'wrkout/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('wrkout:home')) 
    
@login_required
def create_workout(request):
    exercises = Exercise.objects.order_by('Name')
    form = WorkoutForm()
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        difficulty = 0
        count = 0
        if form.is_valid():
            workout = form.save(commit=False)
            workout.CreatorID = UserProfile.objects.get(UserID=request.user.id)
            workout.Date = timezone.now()
            workout.save()
            exerciseSlugs = request.POST.getlist('exerciseSlugs')
            NoOfReps = request.POST.getlist('NoOfReps')
            for i in range(0,len(exerciseSlugs)):
                exercise = Exercise.objects.get(Slug=exerciseSlugs[i])
                difficulty += exercise.Difficulty
                count += 1
                ExerciseID = Exercise.objects.get(ExerciseID=exercise.ExerciseID)
                sets = Set.objects.create(ExerciseID=ExerciseID,NoOfReps=int(NoOfReps[i]))
                workout.Sets.add(sets)
            workout.Difficulty = math.floor(difficulty/count)
            workout.save(update_fields = ['Difficulty'])
            return redirect(reverse('wrkout:home'))
        else:
            print(form.errors)
            
    return render(request, 'wrkout/create_workout.html', {'workout_form': form, 'exercises': exercises})
    
@login_required    
def create_exercise(request):
    form = ExerciseForm()
    if request.method == 'POST':
        print(request.POST)
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.CreatorID = UserProfile.objects.get(UserID=request.user.id)
            exercise.Date = timezone.now()
            if 'DemoImage' in request.FILES:
                exercise.DemoImage = request.FILES['DemoImage']
            exercise.save()
            return redirect(reverse('wrkout:home'))
        else:
            print(form.errors)
            
    return render(request, 'wrkout/create_exercise.html', {'exercise_form': form})

@login_required
def save_workout(request, workout_Name_Slug):
    try:
        workout_to_save = Workout.objects.get(Slug=workout_Name_Slug)
    except Workout.DoesNotExist:
        return HttpResponse("Sorry, something went wrong!")

    logged_in_profile = UserProfile.objects.get(UserAccount=request.user)
    logged_in_profile.SavedWorkouts.add(workout_to_save)

    return redirect(reverse('wrkout:show_workout', kwargs={'workout_Name_Slug': workout_Name_Slug}))

@login_required
def unsave_workout(request, workout_Name_Slug):
    try:
        workout_to_unsave = Workout.objects.get(Slug=workout_Name_Slug)
    except Workout.DoesNotExist:
        return HttpResponse("Sorry, something went wrong!")
    
    logged_in_profile = UserProfile.objects.get(UserAccount=request.user)
    logged_in_profile.SavedWorkouts.remove(workout_to_unsave)

    return redirect(reverse('wrkout:show_workout', kwargs={'workout_Name_Slug': workout_Name_Slug}))

@login_required
def edit_profile(request, username):
    try:
        profile_to_edit = UserProfile.objects.get(UserAccount=request.user)
    except UserProfile.DoesNotExist:
        return HttpResponse("Trying to edit a profile that doesn't exist")

    print(profile_to_edit.UserAccount == request.user)
    
    if request.method == 'POST':
        user_form = EditUserForm(request.POST)
        profile_form = EditProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            if request.POST['username']:
                request.user.username = request.POST['username']
            if request.POST['email']:
                request.user.email = request.POST['email']
            if request.POST['password']:
                request.user.set_password(request.POST['password'])
            if 'ProfilePicture' in request.FILES:
                profile_to_edit.ProfilePicture = request.FILES['ProfilePicture']

            request.user.save()
            profile_to_edit.save()

            return redirect(reverse('wrkout:profile', kwargs={'username': profile_to_edit.Slug}))
        else:
            return render(request, 'wrkout/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        return render(request, 'wrkout/edit_profile.html', {
            'user_form': EditUserForm(),
            'profile_form': EditProfileForm(),
        })

@login_required
def delete_exercise(request, exercise_Name_Slug):
    try:
        exercise_to_delete = Exercise.objects.get(Slug=exercise_Name_Slug)
    except Exercise.DoesNotExist:
        return HttpResponse("Tried to delete an exercise that did not exist.")

    if (exercise_to_delete.CreatorID.UserAccount == request.user):
        exercise_to_delete.delete()
        return redirect(reverse('wrkout:home'))
    else:
        return HttpResponse("You do not have permission to delete this exercise")

@login_required
def delete_workout(request, workout_Name_Slug):
    try:
        workout_to_delete = Workout.objects.get(Slug=workout_Name_Slug)
    except Workout.DoesNotExist:
        return HttpResponse("Tried to delete an workout that did not exist")

    if (workout_to_delete.CreatorID.UserAccount == request.user):
        workout_to_delete.delete()
        return redirect(reverse('wrkout:home'))
    else:
        return HttpResponse("You do not have permission to delete this workout")