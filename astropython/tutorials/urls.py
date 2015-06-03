from django.conf.urls import patterns,url,include

from .models import Tutorial,CodeSnippet,EducationalResource,TutorialSeries,SeriesTutorial
from .views import start_step,intermediate_step,finish_step


urlpatterns = patterns('',
    url(r'^resources/create/$',start_step,{'model':EducationalResource},name="creation_start_educationalresource"),
    url(r'^resources/create/intermediate/(?P<slug>[\w-]+)/$',intermediate_step,{'model':EducationalResource},name="creation_intermediate_educationalresource"),
    url(r'^resources/create/finish/(?P<slug>[\w-]+)/$',finish_step,{'model':EducationalResource},name="creation_finish_educationalresource"),
    url(r'^snippets/create/$',start_step,{'model':CodeSnippet},name="creation_start_codesnippet"),
    url(r'^snippets/create/intermediate/(?P<slug>[\w-]+)/$',intermediate_step,{'model':CodeSnippet},name="creation_intermediate_codesnippet"),
    url(r'^snippets/create/finish/(?P<slug>[\w-]+)/$',finish_step,{'model':CodeSnippet},name="creation_finish_codesnippet"),
    url(r'^tutorials/create/$',start_step,{'model':Tutorial},name="creation_start_tutorial"),
    url(r'^tutorials/create/intermediate/(?P<slug>[\w-]+)/$',intermediate_step,{'model':Tutorial},name="creation_intermediate_tutorial"),
    url(r'^tutorials/create/finish/(?P<slug>[\w-]+)/$',finish_step,{'model':Tutorial},name="creation_finish_tutorial"),
    url(r'^tutorials/series/create/$',start_step,{'model':TutorialSeries},name="creation_start_tutorialseries"),
    url(r'^tutorials/series/(?P<slug>[\w-]+)/add/$',start_step,{'model':SeriesTutorial},name="creation_start_seriestutorial"),
    url(r'^tutorials/series/(?P<slug_series>[\w-]+)/add/(?P<slug>[\w-]+)/complete$',intermediate_step,{'model':SeriesTutorial},name="creation_intermediate_seriestutorial"),
    )

