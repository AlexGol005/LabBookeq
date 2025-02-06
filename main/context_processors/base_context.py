from django.contrib.auth.models import User

from main.models import News, Ad


def last_news(request):
    news = News.objects.last()
    return {
        'last_news': news
    }

def last_ad(request):
    ad = Ad.objects.last()
    return {
        'last_ad': ad
    }

def USER_HAVE_RIGHTS(request):
    '''что это?'''
    try:
        user = User.objects.get(username=request.user)
        if not user.is_staff:
            USER_HAVE_RIGHTS = True
        if user.is_staff:
            USER = False
    except:
        USER_HAVE_RIGHTS = True
    return {
        'USER_HAVE_RIGHTS': USER_HAVE_RIGHTS
    }

def USER(request):
    '''что это?'''
    try:
        user = User.objects.get(username=request.user)
        if user.is_staff:
            USER = True
        if not user.is_staff:
            USER = False
    except:
        USER = True
    return {
        'USER': USER
    }




