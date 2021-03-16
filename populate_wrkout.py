import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wrkout_project.settings')

import django
django.setup()

from wrkout.models import Exercise, Workout, UserProfile, Set
from django.contrib.auth.models import User
from datetime import datetime

def populate():

    useraccounts = [{'username':'testname',
                     'password':'testpassword',
                     'email':'testemail@gmail.com'},]

    
    
    exercises = [{'name':'test exercise', 
                  'description':'test description',
                  'difficulty':3,
                  'likes':12,
                  'creatorname':'testname',
                  'date':'2021-03-16'},]

    sets=[{'exercisename':'test exercise', #SetID = 1
           'noofreps':'12'},
          {'exercisename':'test exercise', #SetID = 2
           'noofreps':'6'},]
    
    workouts = [] 

    for user in useraccounts:
        add_user(user['username'],user['password'],user['email'])

    for exercise in exercises:
        add_exercise(exercise['name'],exercise['description'],exercise['difficulty'],exercise['likes'],exercise['creatorname'],exercise['date'])

    for a_set in sets:
        add_set(a_set['exercisename'],a_set['noofreps'])
    
    

        

def add_user(username, password, email):
    try:
        useraccount = User.objects.create_user(username, password)
        userprofile=UserProfile.objects.get_or_create(UserAccount=useraccount,UserID=useraccount.id)[0]
    except:
        useraccount = User.objects.get(username=username, password=password)
        userprofile=UserProfile.objects.get_or_create(UserAccount=useraccount,UserID=useraccount.id)[0]
    useraccount.username=username
    useraccount.password=password
    useraccount.email=email
    useraccount.save()
    return useraccount


def add_exercise(name, description, difficulty, likes, creatorname, date=datetime.now()):
    creatorid=User.objects.get(username=creatorname).id
    creator=UserProfile.objects.get(UserID=creatorid)
    exercise = Exercise.objects.get_or_create(Name=name, Description=description, Difficulty=difficulty, Likes=likes, CreatorID=creator, Date=datetime.now())[0]
    exercise.Name=name
    exercise.Description=description
    exercise.Difficulty=difficulty
    exercise.Date=date
    exercise.Likes=likes
    exercise.CreatorID=creator
    exercise.save()
    return exercise

def add_set(exercisename, noofreps):
    exerciseid=Exercise.objects.get(Name=exercisename)
    a_set = Set.objects.get_or_create(ExerciseID=exerciseid, NoOfReps=noofreps)[0]
      

    

 
if __name__ == '__main__':
    print('Starting wrkout population script...')
    populate()
