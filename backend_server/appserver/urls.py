import os
from django.conf.urls import url, include
from appserver import views as app_view
from rest_framework_jwt.views import obtain_jwt_token


urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^home/$', app_view.Home.as_view()),
    url(r'^task/$',app_view.TaskList.as_view()),
    url(r'^task/(?P<pk>\d+)/$', app_view.TaskDetail.as_view()),
    url(r'^tag/$',app_view.TagList.as_view()),
    url(r'^child-task/(?P<pk>\d+)/$', app_view.ChildTaskDetail.as_view()),
    url(r'^undelete-task/(?P<pk>\d+)/$', app_view.TaskUndo.as_view()),
    url(r'^status-update/(?P<pk>\d+)/(?P<state>\w+)/$', app_view.TaskStatusUpdate.as_view()),

]