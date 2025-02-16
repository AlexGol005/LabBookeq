from django.utils.deprecation import MiddlewareMixin


class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Do something with request.user
        if request.user.is_authenticated:
            # print(f"Current user: {request.user.username}")
        return request.user

  
