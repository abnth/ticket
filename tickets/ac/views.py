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
    
def submit_ticket(request):
    context=RequestContext(request)
    if(request.method=="POST"):
                    data = request.POST.copy() 
                    #data=request.POST
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
                    data['user_id']=request.user #returns a user object if the user is logged in. @login_required is thus necessary
                    category_selected=data['help_topic']
                    data['help_topic']=Category.objects.filter(category=category_selected)
                    from django.db.models import Max
                    last_ticket=int(Ticket.objects.all().aggregate(Max('ticket_id'))['ticket_id__max'])
                    data['ticket_id']=last_ticket+1
                    print data
                    user_form=SubmitTicketForm(data)
                    if user_form.is_valid():
                            user_form.save()
                            return HttpResponse("Saved successfully")
                    else:
                            return HttpResponse("Saved unsuccessfully")
                            print user_form.errors
    else:
                    user_form=SubmitTicketForm()
    return render_to_response(
                        'submit_ticket.html',
                        {'user_form': user_form},
                        context)
        
        
    