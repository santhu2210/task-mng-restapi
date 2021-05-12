from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserLogin(models.Model):
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField()


class Tag(models.Model):
	name = models.CharField(max_length=48)

	def __str__(self):
		return self.name


class Task(models.Model):
	title = models.CharField(max_length=1500, blank=True)
	parent_task = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
	assigned_user = models.ForeignKey(User, related_name='assign_person')	
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, related_name='creating_person')	
	is_delete = models.BooleanField(default=False)
	tags = models.ManyToManyField(Tag, blank=True)
	state = models.CharField(max_length=100, default='TODO')

	def __str__(self):
		return self.title