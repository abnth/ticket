from PIL import Image as PImage
from ac.models import *
from ac.forms import SubmitTicketForm
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from ac.models import Ticket
import datetime
from datetime import timedelta
from django.db.models import Max
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from ac.forms import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required



def main(request):
    """Main listing."""
    tickets = Ticket.objects.all()
    return render_to_response("d.html",dict(tickets=tickets))

def display(request, id):      
     threads= Ticket.objects.get(pk=id)
     return render_to_response("display.html", dict(threads=threads))

#remove this

#class Ticket(models.Model):
#	user_id=models.ForeignKey(User)
#	topic_id=models.ForeignKey(Category)
#	message=models.TextField()
#	ticket_id=models.IntegerField()
#	#file_uploads=models.FileField(upload_to='tickets/file' , blank=True)
#	created_date_time=models.DateTimeField(auto_now_add=True)
#	overdue_date_time=models.DateTimeField(auto_now_add=True)
#	closed_date_time=models.DateTimeField(auto_now_add=True)
#	status=models.IntegerField()
#	reopened_date_time=models.DateTimeField(auto_now_add=True)
#	topic_priority=models.IntegerField()
#	duration_for_reply=models.IntegerField()
#remove this
@login_required  
def submit_ticket(request):
    context=RequestContext(request)
    if(request.method=="POST"):
                    print request.POST
                    print "________________________\n"
                    data = request.POST.copy() 
                    #data=request.POST
                    print data
                    print "\n"
                    print request.user.email
                    data['created_date_time']=datetime.datetime.now()
                    data['overdue_date_time']=datetime.datetime.now()
                    Date=datetime.datetime.now()
                    Enddate=Date+datetime.timedelta(days=1)
                    data['overdue_date_time']=Enddate
                    data['closed_date_time']=Enddate
                    data['status']=0 # 0 means that the ticket is still open and not yet answered
                    data['reopened_date_time']=Enddate
                    data['topic_priority']=2 # 2 is the default priority of medium
                    data['duration_for_reply']=24 #in hours
                    if request.user.is_authenticated():
                        print request.user
                        data['user_id']=request.user
                        #returns a user object if the user is logged in. @login_required is thus necessary
                    else:
                        return HttpResponse("you need to be a valid user to submit a ticket. click <a href=''>here</a> to go to the login page")
                    category_selected=data['help_topic']
                    data['help_topic']=Category.objects.filter(category=category_selected)
                    from django.db.models import Max
                    last_ticket=int(Ticket.objects.all().aggregate(Max('ticket_id'))['ticket_id__max'])
                    data['ticket_id']=last_ticket+1
                    #if 'submit' in data: del data['submit']
                    #if 'csrfmiddlewaretoken' in data: del data['csrfmiddlewaretoken']
                    
                    #user_form=SubmitTicketForm(data)
                    user_form=SubmitTicketForm(request.POST)
                    #how to validate the form for yourself
                    if user_form.is_valid():
                            user_form.save()
                            return HttpResponse("Saved successfully")
                    else:
                            print data
                            return HttpResponse("Saved unsuccessfully")
                            print "the errors are"
                            print user_form.errors
    else:
                    user_form=SubmitTicketForm()
    return render_to_response(
                        'submit_ticket.html',
                        {'user_form': user_form},
                        context)
        
  
def register(request):
	context=RequestContext(request)
	registered = False
	if(request.method=="POST"):
		#process the form
		user_form=UserForm(data=request.POST)
                print request.POST
		#profile_form=UserProfileForm(data=request.POST)
		if user_form.is_valid():
			user=user_form.save()
			user.set_password(user.password)
			user.save()#hashing the pwd
			#profile=profile_form.save(commit=False)	
			#profile.user=user#This is where we populate the user attribute of the UserProfileForm form, which we hid from users
			#profile.save()
			registered=True
		else:
			print user_form.errors#, profile_form.errors
	else:
		user_form=UserForm()
		#profile_form=UserProfileForm()
	return render_to_response(
            'register.html',
            {'user_form': user_form,  'registered': registered},
            context)#'profile_form': profile_form,

def user_login(request):
    context=RequestContext(request)
    if request.method=="POST":
	#process the login
	#get uname
	username=request.POST['username']
	password=request.POST['password']
	user= authenticate(username=username,password=password)   #authentticate
	if user:
	    if user.is_active:
		login(request,user)
		return HttpResponseRedirect("/ac/")
	    else:
		print "inactive user.cannot login"
		return HttpResponse("your account is inactive can't log you in")
	else:
	    #if auhenticated ie a user object is returned then login and redirect to home; else display the error
	    print "invalid username and password"
	    return HttpResponse("wrong login details")
	    
    else:
	#the form has to be displayed
	return render_to_response('login.html',{},context)
from django.contrib.auth import logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/ac/")      
    