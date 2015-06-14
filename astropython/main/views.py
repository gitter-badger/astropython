from django.shortcuts import render,HttpResponseRedirect,Http404,RequestContext
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

from moderation.helpers import automoderate

import random
from slugify import slugify
import secretballot

from .forms import *
from .models import *
from .utilities import *

def home(request):
	template = 'index.html'
	context = locals()
	return render(request, template, context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def create(request,section,**kwargs):
    model=get_model(section)
    name =get_name(section)
    exclude_fields = get_exclude_fields(model)
    form = get_form(request,exclude_fields,model,kwargs)
    context = RequestContext(request)
    if request.method=="POST":
        if 'save' in request.POST:
            mode="saved"
            for field in form.fields:
                form.fields[field].required = False
            if 'slug' not in kwargs:
                slug="%0.12d" % random.randint(0,999999999999)
                while (model.objects.filter(slug=slug).exists() or model.unmoderated_objects.filter(slug=slug).exists()):
                    slug="%0.12d" % random.randint(0,999999999999)
            else:
                slug=kwargs['slug']
        if form.is_valid():
            instance=form.save(commit=False)
            if 'submit' in request.POST:
                mode="submitted"
                slug=slugify(instance.title)
                while (model.objects.filter(slug=slug).exists() or model.unmoderated_objects.filter(slug=slug).exists()):
                    slug=slug+str(random.randrange(1,1000+1))
                instance.state="submitted"
            instance.slug=slug
            instance.save()
            try:
                user=request.user
                instance.authors.add(request.user)
            except:
                u=User.objects.get_or_create(username="Anonymous")
                instance.authors.add(u[0])
                user=u[0]
            form.save_m2m()
            automoderate(instance,user)
            return render(request,'complete.html',{'section':section,'slug':slug,'mode':mode,'name':name},context)
    return render(request,'creation.html',{'form':form,'name':name},context)

"""
To view a single model instance
"""
def single(request,section,slug,**kwargs):
    model=get_model(section)
    obj=model.objects.get(slug=slug)
    if(obj.state=="raw"):
        if not request.user in obj.authors.all():
            raise Http404
    context = RequestContext(request)
    if(model != SeriesTutorial):
        obj.hits = obj.hits +1
    obj.save()
    if request.method=="GET" and 'edit' in request.GET:
            edit=request.GET['edit']
            if edit=="all":
                edit_field="__all__"
            else:
                edit_field=edit.split(',')
            form= PostForm(model,edit_field,'edit',instance=obj)
            request.session['edit_field']=edit_field
            return render(request,'single.html',{'obj':obj,'section':section,'full_url':request.build_absolute_uri(),'form':form,"mode":"edit"},context)
    if request.method=="POST":
        form= PostForm(model,request.session['edit_field'],'edit',request.POST,instance=obj)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.save()
            form.save_m2m()
            try:
                automoderate(instance,request.user)
            except:
                u=User.objects.get_or_create(username="Anonymous")
                automoderate(instance,u[0])
            return HttpResponseRedirect(reverse('single',kwargs={'section':section,'slug':obj.slug}))
    return render(request,'single.html',{'obj':obj,'section':section,'full_url':request.build_absolute_uri(),"mode":"display"},context)


def single_series(request,slug):
    series=TutorialSeries.objects.get(slug=slug)
    obj=series.seriestutorial_set.order_by('order_id')
    series.hits=series.hits+1
    series.save()
    context = {'obj':obj,'series':series,'name':series.title,'length':len(obj)}
    return render(request,'single-series.html',context)


def vote(request,section,choice,slug):
    model=get_model(section)
    obj=model.objects.get(slug=slug)
    v=model.objects.from_request(request).get(pk=obj.pk)
    token=request.secretballot_token
    if(choice=='upvote'):
        t=1
    else:
        t=-1
    if v.user_vote==t:
        obj.remove_vote(token)
    else:
        obj.add_vote(token,t)
    return HttpResponseRedirect(reverse('single',kwargs={'slug':slug,'section':section}))

"""
General listing of all sections
"""

def all(request,section,display_type,**kwargs):
    model=get_model(section)
    name=get_name(section)
    if display_type=="all":
        obj_list=model.objects.all().filter(state="submitted")
    elif display_type=="latest":
        obj_list=model.objects.all().filter(state="submitted").order_by('-created')
    elif display_type=="popular":
        obj_list=model.objects.all().filter(state="submitted").order_by('-hits')
    length=len(obj_list)
    paginator = Paginator(obj_list,15)
    page = request.GET.get('page')
    try:
        obj=paginator.page(page)
    except:
        obj=paginator.page(1)
    context = {'name':name,'obj':obj,'section':section,'length':length,'range':range(1,obj.paginator.num_pages+1)}
    return render(request,'all.html',context)