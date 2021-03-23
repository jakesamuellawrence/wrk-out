from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from wrkout.models import User, Exercise, Workout, UserProfile
from wrkout.forms import UserForm, ExerciseForm, WorkoutForm, UserProfileForm 
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def test_view(request):
    return render(request, 'wrkout/view_workout.html', {'result': Workout.objects.first})

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
        exercises = Exercise.objects.filter(workout=workout)

        context_dict['exercises'] = exercises
        context_dict['result'] = workout
        
    except Workout.DoesNotExist:
        context_dict['result'] = None
        context_dict['exercises'] = None

    return render(request, 'wrkout/view_workout.html', context_dict['result'])
  
def show_exercise(request, exercise_Name_Slug):
    context_dict = {}

    try:
        exercise = Exercise.objects.get(Slug=exercise_Name_Slug)
        context_dict['result'] = exercise
        
    except Exercise.DoesNotExist:
        context_dict['result'] = None

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
    
    
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.UserAccount = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,'wrkout/register.html',context = {'user_form': user_form,'profile_form': profile_form,'registered': registered})
    
def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('wrkout:home'))
            else:
                return HttpResponse("Your Wrkout account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
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
        if form.is_valid():
            form.save(commit=True)
            return redirect('/wrkout/')
        else:
            print(form.errors)
            
    return render(request, 'wrkout/create_workout.html', {'workout_form': form, 'exercises': exercises})
    
@login_required    
def create_exercise(request):
    form = ExerciseForm()
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/wrkout/')
        else:
            print(form.errors)
            
    return render(request, 'wrkout/create_exercise.html', {'exercise_form': form})
    