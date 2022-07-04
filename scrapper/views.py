from django.shortcuts import render
from scrapper.models import Job
from scrapper.serializers import JobSerializer
from rest_framework import generics
from django.views.generic import ListView


class JobList(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobListView(ListView):
    model = Job
    template_name = 'scrapper/index.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        jobs = Job.objects.all()
        return jobs
