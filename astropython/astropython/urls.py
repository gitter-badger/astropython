from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from moderation.helpers import auto_discover

from main.views import *

admin.autodiscover()
auto_discover()# from moderation app -alway keep below admin.autodiscover()

urlpatterns = patterns('',
    url(r'^grappelli/', include('grappelli.urls')), #for admin urls
    url('', include('social.apps.django_app.urls', namespace='social')), #for social auth urls
    url(r'^admin/', include(admin.site.urls)), #additional admin urls
    url(r'^search$','main.views.search',name="search"),
    url(r'^$', 'main.views.home', name='home'),#home url
    url(r'^logout/', 'main.views.logout_view', name='logout'),#Sample Templates
    url(r'',include('main.urls')),#Teach and Learn
)

#Access Static Files if in development
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)