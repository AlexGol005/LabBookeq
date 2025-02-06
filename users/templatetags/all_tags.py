from django import template

from django.contrib.auth.models import User

register = template.Library()

# name 'request' is not defined!!!
@register.simple_tag()
def get_USER_HAVE_RIGHTS(request):
    user = User.objects.get(username=request.user)
    USER_HAVE_RIGHTS = user
 
    return  USER_HAVE_RIGHTS  
