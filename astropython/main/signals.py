from django.db.models.signals import post_save,post_init
from django.dispatch import receiver
from django.contrib.auth.models import User,Group
from moderation import signals
from django.core.mail import send_mail

@receiver(post_save,sender=User)
def add_to_preview(sender,instance,**kwargs):
    instance.groups.add(Group.objects.get(name="Preview Users"))

@receiver(signals.post_moderation,dispatch_uid="moderation_approval")
def moderation_approval(sender,instance,status,**kwargs):
    try:
        if instance.state=="submitted":
            subject="AstroPython Post Approved !"
            message="Your post at AstroPython is approved"
            html_m='<hr /><h2 style="text-align:center"><code><tt><span style="font-family:trebuchet ms,helvetica,sans-serif"><strong>AstroPython - Python for Astronomers</strong></span></tt></code></h2><hr /><p>Your Post "'+instance.title+'"&nbsp;&nbsp;has&nbsp;been approved by the Moderators !</p><p>Access it <a href="http://amanjhunjhunwala.pythonanywhere.com'+instance.get_absolute_url()+'">here</a> !</p><p>Thank you,</p><p><strong>AstroPython Team</strong></p><hr /><p style="text-align:right"><span style="font-size:10px">Currently , you cannot unsubscribe to these emails</span></p>'
            from_email="notifications@astropython.org"
            send_mail(subject,message,from_email,[str(user.email) for user in instance.authors.all()], fail_silently=False,html_message=html_m)
    except:
        print "No Email Provided"


@receiver(post_save,dispatch_uid="add_content")
def add_content(sender,instance,created,**kwargs):
    if created==True:
        try:
            subject="New AstroPython Post!"
            message="New post at AstroPython"
            html_m='<hr /><h2 style="text-align:center"><code><tt><span style="font-family:trebuchet ms,helvetica,sans-serif"><strong>AstroPython - Python for Astronomers</strong></span></tt></code></h2><hr /><p>A Post "'+instance.title+'"&nbsp;&nbsp;has&nbsp;been added. It has been auto-approved (preview-phase bypassing) !</p><p>Access it <a href="http://amanjhunjhunwala.pythonanywhere.com'+instance.get_absolute_url()+'">here</a> !</p><p>Thank you,</p><p><strong>AstroPython Team</strong></p><hr /><p style="text-align:right"><span style="font-size:10px">Currently , you cannot unsubscribe to these emails</span></p>'
            from_email="notifications@astropython.org"
            send_mail(subject,message,from_email,["amanjjw@gmail.com"], fail_silently=False,html_message=html_m)
        except:
            print "No Email Provided"