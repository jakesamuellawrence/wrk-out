from wrkout.models import UserProfile

def user_profiles(request):
    if request.user.is_authenticated == False: 
        return {}
    try:
        userprof = UserProfile.objects.get(UserAccount=request.user)
    except UserProfile.DoesNotExist:
        return {}
    
    return {'logged_in_profile': userprof}