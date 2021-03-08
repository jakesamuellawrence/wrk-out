from django.http.response import HttpResponse
from django.shortcuts import render
from wrkout.models import User, Exercise
from datetime import datetime

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
        'wrkout/browse_exercises.html',
        {'exercises': [myFirstWorkout, reallyLongName, legDay]}
    )
