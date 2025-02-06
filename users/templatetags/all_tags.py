from django import template

from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag()
def get_USER_HAVE_RIGHTS():
    user = User.objects.get(username=request.user)
    USER_HAVE_RIGHTS = user
 
    return  USER_HAVE_RIGHTS  
