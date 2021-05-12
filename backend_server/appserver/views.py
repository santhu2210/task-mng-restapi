from django.shortcuts import render
import os
import shutil
from datetime import datetime,timedelta
from ast import literal_eval
import json
import logging
import logging.handlers as handlers
import time

from django.db.models import Q
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User
from rest_framework.views import APIView


from baseproject.about import __version__ as version, __title__ as project_name
from appserver.models import Tag, Task
from appserver.serializers import UserSerializer, TaskSerializer

# Logger Config
logger = logging.getLogger(project_name)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s:%(message)s")

logHandler = handlers.TimedRotatingFileHandler(os.path.join(settings.LOG_DIR, project_name+"_v{}_info.log".format(version)), when='midnight', interval=1, backupCount=0)
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)
logHandler.suffix = "%d-%m-%Y"

errorLogHandler = handlers.TimedRotatingFileHandler(os.path.join(settings.LOG_DIR, project_name+"_v{}_error.log".format(version)), when='midnight', interval=1, backupCount=0)
errorLogHandler.setLevel(logging.ERROR)
errorLogHandler.setFormatter(formatter)
errorLogHandler.suffix = "%d-%m-%Y"

logger.addHandler(logHandler)
logger.addHandler(errorLogHandler)

logger.info("Initializing the User Management API service Main engine...")


class Home(generics.ListCreateAPIView):
	if settings.USE_TOKEN:
		permission_classes = (IsAuthenticated, )
		authentication_classes = (JSONWebTokenAuthentication, )

	def get(self, request, format=None):
		logger.info("Calling home endpoint (GET) url by {}".format(request.user))
		return Response({'success': True,'Message':"Welcome to the Task Management API service!.."}, status=status.HTTP_200_OK)


class TaskList(generics.ListCreateAPIView):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer

	def post(self, request, format=None):
		logger.info("Calling task creating endpoint (POST) url by {}".format(request.data['user_id']))	
		logger.info("request data : {}".format(request.data))
		try:
			title = request.data['title']
			parent_task = request.data['parent_task']
			user_id = request.data['user_id']
			# start = datetime.strptime(request.data['start'], '%H:%M').time()
			tags_list = literal_eval(request.POST.get("tags", str([]))) #if No tags list, created empty tag list assigned by default
			user_id = int(user_id)

			# if parent_task == "self":
			# 	parent_task = None
			if parent_task.isnumeric():
				parent_task = int(parent_task)
				# parent_task_obj = Task.objects.get(id=parent_task)
			else:
				parent_task = None

			user_obj = User.objects.get(id=user_id)

			task_req_data = {"title": title, "parent_task": parent_task, "assigned_user":user_id,"created_at": datetime.now(),
							"created_by":user_id, "is_delete":False, "tags": tags_list, "state":"TODO"}

			task_serializer = TaskSerializer(data=task_req_data)

			if task_serializer.is_valid():
				task_serializer.save()
				logger.info("Task was created on requested datetime ")
				task_response = {'success': True,'Message':"Task was assigned for user {}.".format(user_obj.username)}
				return Response(task_response, status=status.HTTP_201_CREATED)
			else:
				task_response = {'success': False,'Message':task_serializer.errors}
				return Response(task_response, status=status.HTTP_406_NOT_ACCEPTABLE)

		except Exception as e:
			logger.exception("Exception raised at task assigning endpoint : {}".format(str(e)))
			task_response = {'success': False,'Message':"{} Exception raised, Please check the form-data fields".format(str(e))}
			return Response(task_response, status=status.HTTP_406_NOT_ACCEPTABLE)

	def get(self, request, format=None):
		tasks = Task.objects.filter(is_delete=False).order_by('-created_at')
		serializer = TaskSerializer(tasks, many=True)

		return Response({'Tasks':serializer.data}, status=status.HTTP_200_OK)



class TaskDetail(APIView):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer

	def get(self, request, pk, format=None):
		tasks = Task.objects.get(pk=pk)
		serializer = TaskSerializer(tasks)

		return Response({'Task':serializer.data}, status=status.HTTP_200_OK)

	def put(self,request, pk, format=None):
		task = Task.objects.get(pk=pk)
		# ext_tags = task.tags.values_list('id', flat=True)
		ext_tags = [t.id for t in task.tags.all()]

		# removing existing tags (default not required)
		for tgid in ext_tags:
			task.tags.remove(Tag.objects.get(pk=tgid))

		tags_list = literal_eval(request.POST.get("tags", str(ext_tags)))
		# adding new tags (not intersection) only 
		# tags_list = list(set(tags_list) - set(ext_tags))
		for tgid in tags_list:
			task.tags.add(Tag.objects.get(pk=tgid))

		task.title = request.data['title']
		task.user_id = request.data['user_id']
		task.state =  request.data['state']
		parent_task = request.data['parent_task']

		if parent_task.isnumeric():
			parent_task = int(parent_task)
			parent_task_obj = Task.objects.get(id=parent_task)
		else:
			parent_task_obj = None

		task.parent_task = parent_task_obj
		task.save()
		serializer = TaskSerializer(task)

		return Response({'Task':serializer.data}, status=status.HTTP_201_CREATED)

	def delete(self,request, pk, format=None):
		task = Task.objects.get(pk=pk)
		task.is_delete =  True
		task.save()
		serializer = TaskSerializer(task)

		return Response({'Task':serializer.data}, status=status.HTTP_200_OK)

class TagList(generics.ListCreateAPIView):

	def get(self, request, format=None):
		tags = Tag.objects.all().values()

		return Response({'Tags':tags}, status=status.HTTP_200_OK)

class ChildTaskDetail(generics.ListCreateAPIView):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer

	def get(self, request, pk, format=None):
		tasks = Task.objects.filter(parent_task=pk).order_by('-created_at')
		serializer = TaskSerializer(tasks, many=True)

		return Response({'Task':serializer.data}, status=status.HTTP_200_OK)


class TaskUndo(APIView):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer

	def put(self,request, pk, format=None):
		task = Task.objects.get(pk=pk)
		task.is_delete =  False
		task.save()
		serializer = TaskSerializer(task)

		return Response({'Task':serializer.data}, status=status.HTTP_200_OK)

class TaskStatusUpdate(APIView):
	queryset = Task.objects.all()
	serializer_class = TaskSerializer

	def get(self, request, pk, state, format=None):
		task = Task.objects.get(pk=pk)
		task.state = state
		task.save()
		serializer = TaskSerializer(task)

		return Response({'Task':serializer.data}, status=status.HTTP_200_OK)