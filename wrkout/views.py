from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from wrkout.models import User, Exercise, Workout
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def test_view(request):
    creativeUser = User.objects.get_or_create(
        Username="CreativeUserNameHere"
    )[0]
    myFirstWorkout = Exercise.objects.get_or_create(
        CreatorID=creativeUser,
        Name='My First Workout',
        Difficulty=1,
        Date=datetime.today().strftime('%Y-%m-%d'),
        Likes=12
    )[0]

    captainMysterious = User.objects.get_or_create(
        Username="CaptainMysterious"
    )[0]
    reallyLongName = Exercise.objects.get_or_create(
        CreatorID=captainMysterious,
        Name='This Workout has a really really really really really really really really really really really really long name',
        Difficulty=2,
        Date="2021-01-27",
        Likes=-17
    )[0]

    muscleMan = User.objects.get_or_create(
        Username="xXMuscleManXx",
    )[0]
    legDay = Exercise.objects.get_or_create(
        CreatorID=muscleMan,
        Name="Leg Day Xtreme",
        Difficulty=5,
        Date="2021-03-01",
        Likes=104
    )[0]

    return render(request, 
        'wrkout/browse.html',
        {'results': [myFirstWorkout, reallyLongName, legDay]}
    )
    
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
                return redirect(reverse('wrkout:show_category',kwargs={'category_name_slug':category_name_slug}))
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