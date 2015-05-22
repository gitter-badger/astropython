from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager

from djangoratings.fields import RatingField
from epiced.models import EpicEditorField
from tinymce import models as tinymce_models

from astropython.settings import STATE_CHOICES

class Base(models.Model):
    categories = models.ManyToManyField('category.Category')
    title = models.CharField(max_length=200)
    #optional logo
    desciption = models.TextField(null=True,blank=True)
    authors = models.ManyToManyField(User,blank=True,null=True)
    slug = models.SlugField(unique=True)
    state = models.CharField(max_length=60,choices=STATE_CHOICES,default='raw')
    tags=TaggableManager()
    rating=RatingField(range=5)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)  # when first revision was created
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)  # when last revision was created (even if not published)
    published = models.DateTimeField(null=True, blank=True,editable=False)  # when last published

    class Meta:
        abstract = True



class MarkdownTutorial(Base):
    body = EpicEditorField()

    def __unicode__(self):
		return self.title

class WYSIWYGTutorial(Base):
    body = tinymce_models.HTMLField()

    def __unicode__(self):
		return self.title

class CodeTutorial(Base):
    body = models.TextField(blank=False)
    notes = EpicEditorField()

    def __unicode__(self):
		return self.title

class TutorialSeries(Base):
    mtutorials = models.ManyToManyField(MarkdownTutorial,null=True)
    wtutorials = models.ManyToManyField(WYSIWYGTutorial,null=True)
    ctutorials = models.ManyToManyField(CodeTutorial,null=True)

    def __unicode__(self):
		return self.title

