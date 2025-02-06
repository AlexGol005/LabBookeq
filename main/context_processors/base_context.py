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



def USER1(request):
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




