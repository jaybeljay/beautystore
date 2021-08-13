from .models import Profile


def get_user_account(request):
    if request.user.is_authenticated:
        account = Profile.objects.get(user=request.user)
        return {'account': account}
    else:
        return {'account': None}
