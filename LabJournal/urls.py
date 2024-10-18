from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ajax_select import urls as ajax_select_urls

urlpatterns = [
    path("admin/lookups/", include(ajax_select_urls)),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('users.urls')),
    path('equipment/', include('equipment.urls')),
    path('^', include('django.contrib.auth.urls')),
    path('postbox/', include('contact_form.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('articles/', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.TOOLBAR_DEBUG:
    import debug_toolbar

    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)

    urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
