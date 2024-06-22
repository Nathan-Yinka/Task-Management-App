from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import ListView,FormView
from django.contrib.auth import login, authenticate

from rest_framework import generics

from core.mixins import TaskQueryMixin
from core.permissions import IsAssignedOrReadOnly
from .models import Task
from .serializers import TaskSerializer
from .form import TaskForm,SignUpForm,LoginForm

User = get_user_model()


class TaskListView(ListView):
    model = Task
    template_name = 'auth/auth.html'
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
        

class TaskListApiView(TaskQueryMixin, generics.ListCreateAPIView):
    serializer_class = TaskSerializer
        
class TaskRetreieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAssignedOrReadOnly]
        
        
# -------------------- User Authentication ---------------------------------

class AuthView(FormView):
    template_name = 'auth/auth.html'
    success_url = reverse_lazy("home")
    
    def get_form_class(self):
        form_type = self.request.GET.get('type',None)
        if form_type == 'signup':
            return SignUpForm
        return LoginForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page"] = self.request.GET.get('type',None)
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    
    
    
    
    