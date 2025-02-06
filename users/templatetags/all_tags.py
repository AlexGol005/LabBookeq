from django import template

from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag()
def get_USER_HAVE_RIGHTS():
    try:
        user = User.objects.get(username=request.user)
        USER_HAVE_RIGHTS = 1
    except:
        USER_HAVE_RIGHTS = 2   
    return  USER_HAVE_RIGHTS  
