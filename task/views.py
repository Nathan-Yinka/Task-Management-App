from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic

from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from .models import Task
from .serializers import TaskSerializer
from .form import TaskForm

User = get_user_model()


class TaskListView(generic.ListView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context["completed"] = self.get_completed_task()
        context["in_progress"] = self.get_in_progress_task()
        context["overdue"] = self.get_overdue_task()
        context["form"] = TaskForm()
        
        return context
        
    def get_completed_task(self):
        completed_tasks = Task.objects.completed()
        return completed_tasks
        
    def get_in_progress_task(self):
        in_progress_tasks = Task.objects.in_progress()
        return in_progress_tasks
    
    def get_overdue_task(self):
        overdued_tasks = Task.objects.overdue()
        return overdued_tasks
        

class TaskListApiView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        qs = Task.objects.all()
        status = self.request.query_params.get('status', None)

        if status:
            if status == 'in_progress':
                qs = qs.in_progress()
            elif status == 'completed':
                qs = qs.completed()
            elif status == 'overdue':
                qs = qs.overdue()
        
        return qs
    
    # def list(self,request,*args, **kwargs):
    #     try:
    #         qs = self.get_queryset()
        
    #         completed_tasks = qs.completed()
    #         in_progress_tasks = qs.in_progress()
    #         overdued_tasks = qs.overdue()
            
    #         completed_serializer = self.get_serializer(completed_tasks, many=True)
    #         in_progress_serializer = self.get_serializer(in_progress_tasks, many=True)
    #         overdue_serializer = self.get_serializer(overdued_tasks, many=True)
            
    #         response = {
    #             'completed_tasks': completed_serializer.data,
    #             'in_progress_tasks': in_progress_serializer.data,
    #             'overdue_tasks': overdue_serializer.data
    #         }
            
    #         return Response(response,status=status.HTTP_200_OK)
    #     except Exception as e:
    #         raise APIException(detail=str(e))
        
class TaskRetreieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
        