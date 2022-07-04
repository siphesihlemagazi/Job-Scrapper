from django.urls import path

from .views import *

urlpatterns = [
    path('jobs/', JobList.as_view()),
    path('', JobListView.as_view(), name='index'),
]