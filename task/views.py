from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.db.models.functions import Lower
from django.urls import reverse_lazy
from django.views.generic import ListView,FormView
from django.contrib.auth import login, authenticate

from rest_framework import generics

from core.mixins import TaskQueryMixin
from core.permissions import IsAssignedOrReadOnly
from .models import Task
from .serializers import TaskSerializer,TaskReadSerializer
from .form import SignUpForm,LoginForm

User = get_user_model()


class TaskListView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'
    
    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context["completed_tasks"] = self.get_completed_task()
        context["in_progress_tasks"] = self.get_in_progress_task()
        context["overdue_tasks"] = self.get_overdue_task()
        context["categories"] = self.get_category_list()
        if self.request.user.is_authenticated:
            context['users'] = User.objects.all().exclude(id=self.request.user.id)
        
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
    
    def get_category_list(self):
        categories = Task.objects.annotate(lower_category=Lower('category')).values_list('lower_category', flat=True).distinct()
        return categories
        

class TaskListApiView(TaskQueryMixin, generics.ListCreateAPIView):
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskReadSerializer
        else:
            return TaskSerializer
        
class TaskRetreieveUpdateDeleteApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsAssignedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskReadSerializer
        else:
            return TaskSerializer
        
# -------------------- User Authentication ---------------------------------

class AuthView(FormView):
    template_name = 'auth/auth.html'
    success_url = reverse_lazy("home")
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
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
    
    

    
    
    