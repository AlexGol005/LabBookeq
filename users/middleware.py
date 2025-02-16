from django.utils.deprecation import MiddlewareMixin


class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        return request.user

  
