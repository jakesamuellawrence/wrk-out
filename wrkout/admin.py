from django.contrib import admin

from wrkout.models import Exercise, Workout, UserProfile

class ExerciseAdmin(admin.ModelAdmin):
    list_display=("ExerciseID","CreatorID","Name","Difficulty","Date","Likes")

class WorkoutAdmin(admin.ModelAdmin):
    list_display=("WorkoutID","CreatorID","Name","Difficulty","Date","Likes")

admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Workout, WorkoutAdmin)
