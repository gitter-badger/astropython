"""
Contains forms that we shall use in a particular app
"""
from django import forms
from moderation.forms import BaseModeratedObjectForm
from .models import *

def PostForm(model_type,form_fields,action,*args,**kwargs):
    class PostForm(BaseModeratedObjectForm):
        class Meta:
            model=model_type
            if action=="create":
                exclude=form_fields
            elif action=="edit":
                fields=form_fields

        def __init__(self):
            super(PostForm, self).__init__(*args, **kwargs)

    return PostForm()