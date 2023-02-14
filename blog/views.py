from django.views.generic import ListView

from blog.models import Blog


class BlogView(ListView):
    """ Выводит список всех постов """
    model = Blog
    template_name = 'blog/blog.html'
    context_object_name = 'objects'
    ordering = ['-pk']
    paginate_by = 6
