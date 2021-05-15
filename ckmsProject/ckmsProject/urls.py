from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from publications.views import CategoryListing
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('post/', include('publications.urls')),
    path('', CategoryListing.as_view(), name='post_more_details'),
    path('usersreg/', include('usersreg.urls')),
    path('about/', TemplateView.as_view(template_name="about.html"), name='about'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

