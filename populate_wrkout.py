import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wrkout_project.settings')

import django
django.setup()

from wrkout.models import Exercise, Workout, UserProfile, Set

def populate():
    
    exercises = [] #dictionaries containing exercises go here
    #format is something like {'CreatorID' = CreatorID, 'name' = name,
    #                       'difficulty' = difficulty, 'description' = description, 'date' = date, 'likes' = likes}
    
    workouts = [] #dictionaries containing workouts go here
     
    #format is something like exercises, but it also key 'sets' = {reps:exercise1, reps:exercise2, etc...}
        #                             (will later on create a list of sets from this dictionary)
    
    userprofiles = [] #dictionaries containing user profiles go here
    #format is something like {'SavedWorkouts' = SW, 'LikedWorkouts' = LW, 'LikedExercises' = LE}
    
    
    for ex in exercises:
        CID = ex['CreatorID']
        name = ex['name']
        difficulty = ex['difficulty']
        description = ex['description']
        date = ex['date']
        likes = ex['likes']
        
        add_exercise(CID, name, difficulty, description, date, likes)
        
    for w in workouts:
        
        sets = [] #list of sets...? not sure how many to many field works
        for reps, exercise in w['sets']:
            ExID = exercise.ExerciseID
            s = Set(ExerciseID = ExID, Reps = reps)
            sets.append(s)
        
        CID = w['CreatorID']
        name = w['name']
        difficulty = w['difficulty']
        description = w['description']
        date = w['date']
        likes = w['likes']                       
        
        add_workout(CID, sets, name, description, difficulty, date, likes)
        
    for user in userprofiles:
        
        SW = user['SavedWorkouts']
        LW = user['LikedWorkouts']
        LE = user['LikedExercises']
        
        add_userprofile(SW, LW, LE)
        

def add_exercise(CID, name, difficulty, description, date, likes):
    e = Exercise.get_or_create(CreatorID = CID, Name = name, Difficulty = difficulty,
                               Description = description,Date = date, Likes = likes)
    e.save()
    return e


def add_workout(CID, sets, name, description, difficulty, date, likes):
    w = Workout.get_or_create(CreatorID = CID, Sets = sets, Name = name,
                              Description = description, Difficulty = difficulty, 
                              Date = date, Likes = likes)
    w.save()
    return w
    
    

def add_userprofile(SW, LW, LE):
    user = UserProfile.get_or_create(SavedWorkouts = SW, LikedWorkouts = LW, LikedExercises = LE)
    user.save()
    
    return user
    

 
if __name__ == '__main__':
    print('Starting wrkout population script...')
    populate()
