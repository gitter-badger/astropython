from django.shortcuts import render,HttpResponseRedirect,Http404,RequestContext
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db.models.functions import Lower

from moderation.helpers import automoderate

import feedparser
import secretballot
import watson

from .forms import *
from .models import *
from .utilities import *
from taggit.models import Tag,TaggedItem

def home(request):
	template = 'index.html'
	context = {'posts':get_all_objects("all")[:5]}
	return render(request, template, context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def create(request,section,**kwargs):
    model=get_model(section)
    name =get_name(section)
    tags=model.tags.all()
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
    return render(request,'creation.html',{'form':form,'name':name,'tags': tags})

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
            user=get_user(request)
            instance.save()
            form.save_m2m()
            automoderate(instance,user)
            return HttpResponseRedirect(reverse('single',kwargs={'section':section,'slug':obj.slug}))
    else:
        form=None
    recent=model.objects.all().filter(state="submitted").order_by('-created')[:5]
    return render(request,'single.html',{'obj':obj,'section':section,'full_url':request.build_absolute_uri(),"mode":mode,"form":form,"tags":tags,'page':'single','recent':recent})


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
    t=None
    s=None
    f=None
    message=""
    if 'sort' in request.GET:
        sort=request.GET['sort']
        s=sort
        message+="Ordered by "+sort+"   "
        if sort=="ratings":
            obj_list=model.objects.all().filter(state="submitted").order_by('-total_upvotes')
        elif sort=="alphabetical":
             obj_list=model.objects.all().filter(state="submitted").order_by(Lower('title'))
        elif section=="packages" and sort=="recommended":
                obj_list=model.objects.all().filter(category="Recommended").order_by('-created')
        else:
            obj_list=model.objects.all().filter(state="submitted").order_by('-created')
    else:
        if section=="packages":
             obj_list=model.objects.all().filter(state="submitted").order_by(Lower('title'))
        else:
            obj_list=model.objects.all().filter(state="submitted").order_by('-created')
    if 'tags' in request.GET:
        tags=request.GET['tags']
        t=tags
        if message=="":
            message+="Filtered by tags : "+tags
        else:
            message+=",Filtered by tags : "+tags
        tag=tags.split(',')
        for tag_elem in tag:
            tag_list=[]
            tag_list.append(tag_elem)
            obj_list=obj_list.filter(tags__name__in=tag_list).distinct()
    if 'filter' in request.GET:
        f=request.GET['filter']
        message+="(Showing "+f+" posts)"
        if f=='native':
            obj_list=obj_list.filter(~Q(authors__username__startswith = "Feed")).distinct()
        elif f=='feeds':
            obj_list=obj_list.filter(authors__username__startswith = "Feed").distinct()
    length=len(obj_list)
    if section=="packages":
        paginator = Paginator(obj_list,100)
    else:
        paginator = Paginator(obj_list,15)
    page = request.GET.get('page')
    try:
        obj=paginator.page(page)
    except:
        obj=paginator.page(1)
    tags=[]
    for ob in obj_list:
        tags += ob.tags.all()
    tags=list(set(tags))
    recent=model.objects.all().filter(state="submitted").order_by('-created')[:5]
    get={'tags':t,'filter':f,'sort':s}
    context = {'name':name,'obj':obj,'section':section,'length':length,'message':message,'tags':tags,'range':range(1,obj.paginator.num_pages+1),'page':'all','recent':recent,'get':get}
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

def timeline(request,section):
    object_list=get_all_objects(section)
    context = {'data': list(object_list),'section':section}
    return render(request,'timeline.html',context)

def contact(request):
    if request.POST:
        form=ContactForm(request.POST)
        form.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def update_feed(request):
    update_feeds()
    return render(request,'complete.html',{'state':'feed_update','name':'Feed Update'})

def display_feed_list(request):
    obj_list=Feed.objects.all()
    length=len(obj_list)
    paginator = Paginator(obj_list,10)
    page = request.GET.get('page')
    try:
        obj=paginator.page(page)
    except:
        obj=paginator.page(1)
    context = {'name':'Feed List','obj':obj,'length':length,'range':range(1,obj.paginator.num_pages+1),'page':'all'}
    return render(request,'feed_list.html',context)
