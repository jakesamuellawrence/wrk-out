from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from wrkout.models import User, Exercise, Workout, UserProfile
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def test_view(request):
    creativeUser = User.objects.get_or_create(
        username="CreativeUserNameHere"
    )[0]
    creativeUserProfile = UserProfile.objects.get_or_create(
        UserAccount=creativeUser
    )[0]
    myFirstWorkout = Workout.objects.get_or_create(
        CreatorID=creativeUserProfile,
        Name='My First Workout',
        Difficulty=1,
        Date=datetime.today().strftime('%Y-%m-%d'),
        Likes=12
    )[0]

    return render(request, 
        'wrkout/browse.html',
        {'results': [myFirstWorkout]}
    )

def show_workout(request, category_name_slug):
    context_dict = {}

    try:
        workout = Workout.objects.get(slug=category_name_slug)
        exercises = Exercise.objects.filter(workout=workout)

        context_dict['exercises'] = exercises
        context_dict['workout'] = workout
        
    except Workout.DoesNotExist:
        context_dict['workout'] = None
        context_dict['exercises'] = None

    return render(request, 'wrkout/workout.html', context_dict)
    
def browse_workouts(request):
    workout_list = Workout.objects.order_by('-likes')
    context_dict = {}
    context_dict['workouts'] = workout_list
    response = render(request, 'wrkout/browse.html', context=context_dict)
    return response
    
def browse_exercises(request):
    exercise_list = Exercise.objects.order_by('-likes')
    context_dict = {}
    context_dict['exercises'] = exercise_list
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
            profile.user = user

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
                return redirect(reverse('wrkout:index'))
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
    return redirect(reverse('wrkout:index')) 
    
@login_required    
def create_workout(request, category_name_slug):
    try:
        workout = Workout.objects.get(slug=category_name_slug)
    except Workout.DoesNotExist:
        workout = None
    if workout is None:
        return redirect('/wrkout/')
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if workout:
                page = form.save(commit=False)
                page.workout = workout
                page.views = 0
                page.save()
                return redirect(reverse('wrkout:show_workout',kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'workout': workout}
    return render(request, 'wrkout/create_workout.html', context=context_dict)
    
@login_required    
def create_exercise(request, category_name_slug):
    try:
        exercise = Exercise.objects.get(slug=category_name_slug)
    except Exercise.DoesNotExist:
        exercise = None
    if exercise is None:
        return redirect('/wrkout/')
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if exercise:
                page = form.save(commit=False)
                page.exercise = exercise
                page.views = 0
                page.save()
                return redirect(reverse('wrkout:show_category',kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'exercise': exercise}
    return render(request, 'wrkout/create_exercise.html', context=context_dict)