from django.db import models
from django.db.models import *
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models.signals import post_save
from shared.utils import *

class Ticket(models.Model):
	user_id=models.ForeignKey(User)
	topic_id=models.ForeignKey(Category)
	message=models.TextField()
	ticket_id=models.IntegerField()
	#file_uploads=models.FileField(upload_to='tickets/file' , blank=True)
	created_date_time=models.DateTimeField(auto_now_add=True)
	overdue_date_time=models.DateTimeField(auto_now_add=True)
	closed_date_time=models.DateTimeField(auto_now_add=True)
	status=models.IntegerField()
	reopened_date_time=models.DateTimeField(auto_now_add=True)
	topic_priority=models.IntegerField()
	duration_for_reply=models.IntegerField()
        
        

	def __unicode__(self):
		return unicode(self.user_id)


class Tablet_info(models.Model):
	rcID=models.IntegerField()
	rcName=models.CharField(max_length=100)
	start_tab_id=models.IntegerField()
	end_tab_id=models.IntegerField()
	count=models.IntegerField()
	city=models.CharField(max_length=20)

	def __unicode__(self):
		return self.start_tab_id,self.end_tab_id
