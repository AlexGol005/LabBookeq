from django.views.generic import ListView, TemplateView

from blog.models import Blog


class BlogView(ListView):
    """ Выводит список всех постов """
    model = Blog
    template_name = 'blog/blog.html'
    context_object_name = 'objects'
    ordering = ['-pk']
    paginate_by = 6


class BlogStrView(TemplateView):
    """ выводит отдельный пост """
    model = Blog
    template_name = 'blog/blogstr.html'


    def get_object(self, queryset=None):
        return Blog.objects.get(pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super(BlogStrView, self).get_context_data(**kwargs)
        obj = Blog.objects.get(pk=self.kwargs.get("pk"))
        context['obj'] = obj
        return context

   

