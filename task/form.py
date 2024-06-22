from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages

from .models import Task

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'category', 'assigned_to']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
class SignUpForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        
    def save(self, commit: bool = True):
        user = super().save(commit)
        username = self.cleaned_data.get('username')
        raw_password = self.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        messages.success(self.request, f"Welcome, {username}! Your account has been created successfully.")
        return user
        
class LoginForm(AuthenticationForm):
    
    error_messages = {
    "invalid_login": (
        "Invaild Credentials"
    ),
    "inactive": ("This account is inactive."),
    }
    
    class Meta:
        model = User
        fields = ('username', 'password')
        
    def save(self):
        user = self.get_user()
        login(self.request, user)
        messages.success(self.request, f"Welcome back, {user.username}!")