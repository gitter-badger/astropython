from django.shortcuts import render,HttpResponseRedirect,Http404,RequestContext
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse

from moderation.helpers import automoderate

import secretballot
import watson

from .forms import *
from .models import *
from .utilities import *
from taggit.models import Tag,TaggedItem

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
    form = get_create_form(request,exclude_fields,model,kwargs)
    if request.method=="POST":
        state=set_state(request,form)
        if form.is_valid():
            instance=form.save(commit=False)
            slug = get_slug(request,model,instance.title,kwargs)
            user=get_user(request)
            instance.state=state
            instance.slug=slug
            instance.save()
            instance.authors.add(user)
            form.save_m2m()
            automoderate(instance,user)
            return render(request,'complete.html',{'section':section,'slug':slug,'state':state,'name':name})
    return render(request,'creation.html',{'form':form,'name':name})

"""
To view a single model instance
"""
def single(request,section,slug,**kwargs):
    model=get_model(section)
    name=get_name(section)
    tags=model.tags.all()
    obj=model.objects.get(slug=slug)
    mode="display"
    if request.method=="GET" and 'edit' in request.GET:
        edit=request.GET['edit']
        edit_field=edit.split(',')
        request.session['edit_field']=edit_field
        request.session.modified = True
        form= PostForm(model,edit_field,'edit',instance=obj)
        mode="edit"
    elif request.method=="POST":
        form= PostForm(model,request.session['edit_field'],'edit',request.POST,instance=obj)
        mode="edit"
        if form.is_valid():
            instance=form.save(commit=False)
            instance.hits=instance.hits + 1
            user=get_user(request)
            instance.save()
            form.save_m2m()
            automoderate(instance,user)
            return HttpResponseRedirect(reverse('single',kwargs={'section':section,'slug':obj.slug}))
    else:
        form=None
    popular=model.objects.all().filter(state="submitted").order_by('-hits')[:5]
    recent=model.objects.all().filter(state="submitted").order_by('-created')[:5]
    return render(request,'single.html',{'obj':obj,'section':section,'full_url':request.build_absolute_uri(),"mode":mode,"form":form,"tags":tags,'page':'single','recent':recent,'popular':popular})


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

def all(request,section,**kwargs):
    model=get_model(section)
    name=get_name(section)
    message=""
    if 'sort' in request.GET:
        sort=request.GET['sort']
        message+="Ordered by "+sort+"   "
        if sort=="popularity":
            obj_list=model.objects.all().filter(state="submitted").order_by('-hits')
        elif sort=="ratings":
            obj_list=model.objects.all().filter(state="submitted").order_by('total_upvotes')
        elif sort=="recommended" and section=="packages":
            obj_list=model.objects.all().filter(category="Recommended").order_by('-created')
        else:
            obj_list=model.objects.all().filter(state="submitted").order_by('-created')
    else:
            obj_list=model.objects.all().filter(state="submitted").order_by('-created')
    if 'tags' in request.GET:
        tags=request.GET['tags']
        message+="Filtered by tags : "+tags
        tag=tags.split(',')
        obj_list=obj_list.filter(tags__name__in=tag).distinct()
    length=len(obj_list)
    paginator = Paginator(obj_list,10)
    page = request.GET.get('page')
    try:
        obj=paginator.page(page)
    except:
        obj=paginator.page(1)
    tags = model.tags.all()
    popular=model.objects.all().filter(state="submitted").order_by('-hits')[:5]
    recent=model.objects.all().filter(state="submitted").order_by('-created')[:5]
    context = {'name':name,'obj':obj,'section':section,'length':length,'message':message,'tags':tags,'range':range(1,obj.paginator.num_pages+1),'page':'all','recent':recent,'popular':popular}
    return render(request,'all.html',context)

def search(request):
    if request.GET['q']:
        name="All Sections"
        section="all"
        query=request.GET['q']
        if 'section' in request.GET:
            section=request.GET['section']
            if section=="all":
                results=watson.search(query)
            else:
                sec=[]
                model=get_model(section)
                name=get_name(section)
                sec.append(model)
                results=watson.search(query,models=tuple(sec))
        else:
            results=watson.search(query)
    else:
        return HttpResponseRedirect(reverse('home'))
    length=len(results)
    paginator = Paginator(results,10)
    page = request.GET.get('page')
    try:
        obj=paginator.page(page)
    except:
        obj=paginator.page(1)
    context = {'name':name,'obj':obj,'section':section,'length':length,'range':range(1,obj.paginator.num_pages+1),'query':query}
    return render(request,'search.html',context)

def written(request):
    u=request.user
    message=None
    tutorials_list=u.tutorial_set.all()
    announcements_list=u.announcement_set.all()
    blogs_list=u.blog_set.all()
    edresources_list=u.educationalresource_set.all()
    news_list=u.news_set.all()
    events_list=u.event_set.all()
    packages_list=u.package_set.all()
    snippets_list=u.snippet_set.all()
    wiki_list=u.wiki_set.all()
    if (len(tutorials_list)+len(announcements_list)+len(blogs_list)+len(edresources_list)+len(news_list)+len(events_list)+len(packages_list)+len(snippets_list)+len(wiki_list))==0:
        message="You do not have any posts yet !"
    context={'message':message,'tutorials_list':tutorials_list,'announcements_list':announcements_list,'blogs_list':blogs_list,'edresources_list':edresources_list,'news_list':news_list,'events_list':events_list,'packages_list':packages_list,'snippets_list':snippets_list,'wiki_list':wiki_list}
    return render(request,'written.html',context)
