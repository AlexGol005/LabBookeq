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
        if request.user.has_perm('equipment.add_equipment') or request.user.is_superuser:
            USER_HAVE_RIGHTS = True
        else:
            USER_HAVE_RIGHTS = False
    except:
        USER_HAVE_RIGHTS = False
    return {
        'USER_HAVE_RIGHTS': USER_HAVE_RIGHTS
    }




