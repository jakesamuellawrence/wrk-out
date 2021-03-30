from wrkout.models import UserProfile

def user_profiles(request):
    if request.user.is_authenticated == False: 
        return {}

    # This will automatically create a profile for any user that doesn't have one (e.g. admins)
    userprof = UserProfile.objects.get_or_create(UserAccount=request.user)[0]
    
    return {'logged_in_profile': userprof}