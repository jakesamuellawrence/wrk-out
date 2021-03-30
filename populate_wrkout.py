import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wrkout_project.settings')

import django
django.setup()

from wrkout.models import Exercise, Workout, UserProfile, Set
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.hashers import make_password

def populate():

    useraccounts = [{'username':'TeamWrkOut',
                     'password':'WrkOutPassword',
                     'email':'TeamWrkOut@gmail.com',
                     'profilepicture':'TeamWrkOut.png'},
                    {'username':'CreativeUsernameHere',
                     'password':'CreativePassword',
                     'email':'CreativeUsernameHere@gmail.com',
                     'profilepicture':'CreativeUsernameHere.png'},
                    {'username':'CaptainMysterious',
                     'password':'CaptainPassword',
                     'email':'CaptainMysterious@gmail.com',
                     'profilepicture':'CaptainMysterious.png'},
                    {'username':'xXMuscleManXx',
                     'password':'MusclePassword',
                     'email':'xXMuscleManXx@gmail.com',
                     'profilepicture':'xXMuscleManXx.png'}]
    
    exercises = [{'name':'Star Jump', 
                  'description':'Jump to a position with the legs spread wide and the hands going overhead and then return to a position with the feet together and the arms at the sides.',
                  'difficulty':1,
                  'likes':39,
                  'creatorname':'TeamWrkOut',
                  'exerciseimage':'star-jump.png',
                  'date':'2021-03-15'},
                 {'name':'Push Up', 
                  'description':'In the prone position by raise and lower your body with the straightening and bending of your arms while keeping the back straight and supporting the body on your hands and toes.',
                  'difficulty':3,
                  'likes':24,
                  'creatorname':'TeamWrkOut',
                  'exerciseimage':'push-up.png',
                  'date':'2021-03-16'},
                 {'name':'Squat', 
                  'description':'Stand straight and lower down as if sitting on an invisible chair, straighten yout legs to lift back up.',
                  'difficulty':2,
                  'likes':13,
                  'creatorname':'xXMuscleManXx',
                  'exerciseimage':'squat.png',
                  'date':'2021-03-10'},
                 {'name':'Car Lift', 
                  'description':'It is what its called, lift up a car.',
                  'difficulty':5,
                  'likes':-4,
                  'creatorname':'xXMuscleManXx',
                  'exerciseimage':'',
                  'date':'2021-03-17'},
                 {'name':'Pull Up', 
                  'description':'Grip an overhead bar and lift your body until your chin is above the bar.',
                  'difficulty':4,
                  'likes':12,
                  'creatorname':'CreativeUsernameHere',
                  'exerciseimage':'pull-up.png',
                  'date':'2021-03-12'},
                 {'name':'Burpee', 
                  'description':'A burpee is a two-part exercise, firstly lower yourself down into a press up, then jump up in the air.',
                  'difficulty':4,
                  'likes':28,
                  'creatorname':'CreativeUsernameHere',
                  'exerciseimage':'burpee.png',
                  'date':'2021-03-09'},
                 {'name':'5km Run', 
                  'description':'Run a distance of five kilometres.',
                  'difficulty':4,
                  'likes':9,
                  'creatorname':'CaptainMysterious',
                  'exerciseimage':'',
                  'date':'2021-03-14'},
                 {'name':'Mud Crawl', 
                  'description':'Crawl 10m through mud and rain.',
                  'difficulty':5,
                  'likes':-12,
                  'creatorname':'CaptainMysterious',
                  'exerciseimage':'',
                  'date':'2021-03-17'},]

    sets=[{'exercisename':'Star Jump', #SetID = 1
           'noofreps':'20'},
          {'exercisename':'Push Up', #SetID = 2 
           'noofreps':'6'},
          {'exercisename':'Push Up', #SetID = 3 
           'noofreps':'12'},
          {'exercisename':'Squat', #SetID = 4 
           'noofreps':'8'},
          {'exercisename':'Car Lift', #SetID = 5 
           'noofreps':'1'},
          {'exercisename':'Pull Up', #SetID = 6 
           'noofreps':'3'},
          {'exercisename':'Burpee', #SetID = 7 
           'noofreps':'10'},
          {'exercisename':'5km Run', #SetID = 8 
           'noofreps':'1'},
          {'exercisename':'Mud Crawl', #SetID = 9 
           'noofreps':'2'},]
    
    workouts = [{'name':'Our First Workout',
                'description':'The first workout we have made!',
                'difficulty':2,
                'likes':21,
                'creatorname':'TeamWrkOut',
                'date':'2021-03-18',
                'sets':[1,2]},
                {'name':'Leg Day Burner',
                'description':'A workout to set your legs alight.',
                'difficulty':5,
                'likes':-2,
                'creatorname':'xXMuscleManXx',
                'date':'2021-03-20',
                'sets':[4,5,8]},
                {'name':'Cardio Extreme',
                'description':'This will get your heart pumping.',
                'difficulty':3,
                'likes':8,
                'creatorname':'CreativeUsernameHere',
                'date':'2021-03-14',
                'sets':[1,8,7,8]},
                {'name':'Marine Entry',
                'description':'A royal marine level workout.',
                'difficulty':4,
                'likes':16,
                'creatorname':'CaptainMysterious',
                'date':'2021-03-10',
                'sets':[1,3,6,9,3]},]

    savedworkouts = [{'username':'TeamWrkOut',
                      'savedworkouts':["Marine Entry","Cardio Extreme","Leg Day Burner"]},
                     {'username':'CaptainMysterious',
                      'savedworkouts':["Cardio Extreme","Our First Workout"]},
                     {'username':'CreativeUsernameHere',
                      'savedworkouts':["Marine Entry"]},
                     {'username':'xXMuscleManXx',
                      'savedworkouts':["Our First Workout"]},]

    likedexercises = [{'username':'TeamWrkOut',
                       'exercises':['Squat','Pull Up','5km Run']},
                      {'username':'CaptainMysterious',
                       'exercises':['Push Up','Car Lift']},
                      {'username':'CreativeUsernameHere',
                       'exercises':['Star Jump','Push Up']},
                      {'username':'xXMuscleManXx',
                       'exercises':['Push Up']},]

    likedworkouts = [{'username':'TeamWrkOut',
                       'workouts':['Leg Day Burner','Cardio Extreme','Marine Entry']},
                      {'username':'CaptainMysterious',
                       'workouts':['Cardio Extreme','Leg Day Burner']},
                      {'username':'CreativeUsernameHere',
                       'workouts':['Our First Workout']},
                      {'username':'xXMuscleManXx',
                       'workouts':['Marine Entry']},]

    for user in useraccounts:
        add_user(user['username'],user['password'],user['email'], user['profilepicture'])

    for exercise in exercises:
        add_exercise(exercise['name'],exercise['description'],exercise['difficulty'],exercise['likes'],exercise['creatorname'],exercise['exerciseimage'],exercise['date'])

    for a_set in sets:
        add_set(a_set['exercisename'],a_set['noofreps'])

    for workout in workouts:
        add_workout(workout['name'],workout['description'],workout['difficulty'],workout['likes'],workout['creatorname'],workout['sets'],workout['date'])

    for savedworkout in savedworkouts:
        add_savedworkouts(savedworkout['username'],savedworkout['savedworkouts'])

    for likedexercise in likedexercises:
        add_likedexercises(likedexercise['username'],likedexercise['exercises'])

    for likedworkout in likedworkouts:
        add_likedworkouts(likedworkout['username'],likedworkout['workouts'])
    
    

def add_user(username, password, email, profilepicture):
    try:
        useraccount = User.objects.create_user(username)
        userprofile=UserProfile.objects.get_or_create(UserAccount=useraccount,UserID=useraccount.id)[0]
    except:
        useraccount = User.objects.get(username=username)
        userprofile=UserProfile.objects.get_or_create(UserAccount=useraccount,UserID=useraccount.id)[0]
    useraccount.username=username
    useraccount.password= make_password(password)
    useraccount.email=email
    if profilepicture!="":
        userprofile.ProfilePicture="profile_images/"+profilepicture
    useraccount.save()
    userprofile.save()
    return useraccount, userprofile


def add_exercise(name, description, difficulty, likes, creatorname, exerciseimage, date=datetime.now()):
    creatorid=User.objects.get(username=creatorname).id
    creator=UserProfile.objects.get(UserID=creatorid)
    exercise = Exercise.objects.filter(Name=name, Description=description, CreatorID=creator)
    if exercise.exists():
        pass
    else:
        exercise = Exercise.objects.create(Name=name, Description=description, Difficulty=difficulty, Likes=likes, CreatorID=creator, DemoImage=exerciseimage, Date=datetime.now())
        exercise.Name=name
        exercise.Description=description
        exercise.Difficulty=difficulty
        if exerciseimage != "":
            exercise.DemoImage="exercise_images/"+exerciseimage
        exercise.Date=date
        exercise.Likes=likes
        exercise.CreatorID=creator
        exercise.save()
    return exercise

def add_set(exercisename, noofreps):
    exerciseid=Exercise.objects.get(Name=exercisename)
    a_set = Set.objects.get_or_create(ExerciseID=exerciseid, NoOfReps=noofreps)[0]
    a_set.ExerciseID=exerciseid
    a_set.NoOfReps=noofreps
    a_set.save()
    return a_set
      
                                            
def add_workout(name, description, difficulty, likes, creatorname, sets, date=datetime.now()):
    creatorid=User.objects.get(username=creatorname).id
    creator=UserProfile.objects.get(UserID=creatorid)
    workout = Workout.objects.filter(Name=name, Description=description, Difficulty=difficulty, Likes=likes, CreatorID=creator, Date=date)
    if workout.exists():
        pass
    else:
        workout = Workout.objects.create(Name=name, Description=description, Difficulty=difficulty, Likes=likes, CreatorID=creator, Date=date)
        for setid in sets:
            a_set = Set.objects.get(SetID=setid)
            workout.Sets.add(a_set)
        workout.save()
    return workout

def add_savedworkouts(username, savedworkouts):
    useraccount = User.objects.get(username=username)
    userprofile=UserProfile.objects.get(UserAccount=useraccount,UserID=useraccount.id)
    for workoutname in savedworkouts:
        savedworkout = Workout.objects.get(Name=workoutname)
        userprofile.SavedWorkouts.add(savedworkout)

def add_likedexercises(username, likedexercises):
    useraccount = User.objects.get(username=username)
    userprofile=UserProfile.objects.get(UserAccount=useraccount,UserID=useraccount.id)
    for exercisename in likedexercises:
        likedexercise = Exercise.objects.get(Name=exercisename)
        userprofile.LikedExercises.add(likedexercise)

def add_likedworkouts(username, likedworkouts):
    useraccount = User.objects.get(username=username)
    userprofile=UserProfile.objects.get(UserAccount=useraccount,UserID=useraccount.id)
    for workoutname in likedworkouts:
        likedworkout = Workout.objects.get(Name=workoutname)
        userprofile.LikedWorkouts.add(likedworkout)
    

 
if __name__ == '__main__':
    print('Starting wrkout population script...')
    populate()
