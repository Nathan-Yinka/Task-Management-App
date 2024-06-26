from django.db import models
from django.db.models import Case,When,IntegerField,Q
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

User = get_user_model()

class TaskQuerySet(models.QuerySet):
  
    def search(self, query=None, status=None, priority=None, start_date=None, end_date=None, category=None, sort_by=None):
        filters = Q()
        
        if query:
            filters &= Q(title__icontains=query) | Q(description__icontains=query)
        
        if status:
            filters &= Q(status__iexact=status)
        
        if priority:
            filters &= Q(priority__iexact=priority)
        
        if start_date and end_date:
            filters &= Q(due_date__date__range=(start_date, end_date))
        
        if category:
            filters &= Q(category__iexact=category)
            
        qs = self.filter(filters)
            
        if sort_by:
            if sort_by == "priority":
                qs = qs.order_by_priority()
            else:
                qs = qs.order_by(sort_by)
        
        return qs

    def completed(self):
        return self.filter(status="Completed").order_by_priority()
      
    def in_progress(self):
        return self.filter(status="In Progress").order_by_priority()
      
    def overdue(self):
        return self.filter(status="Overdue").order_by_priority()
      
    def all(self):
        qs = super().all()
        return qs.order_by_priority()
      
    def order_by_priority(self):
        priority_order = Case(
            When(priority='Low', then=1),
            When(priority='Medium', then=2),
            When(priority='High', then=3),
            output_field=IntegerField(),
        )
        return self.annotate(priority_order=priority_order).order_by('-priority_order',"-due_date")
      
  
class TaskManager(models.Manager):

    def get_queryset(self):
        return TaskQuerySet(self.model,using=self._db)
      
    def completed(self):
        return self.get_queryset().completed()
      
    def in_progress(self):
        return self.get_queryset().in_progress()
      
    def overdue(self):
        return self.get_queryset().overdue()
      
    def order_by_priority(self):
        return self.get_queryset().order_by_priority()
      
    def search(self, query=None, status=None, priority=None, start_date=None, end_date=None, category=None, sort_by=None):
        return self.get_queryset().search(query=query, status=status, priority=priority, start_date=start_date, 
            end_date=end_date, category=category, sort_by=sort_by)


class Task(models.Model):
    
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Overdue', 'Overdue'),
        ]
      
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
      
      
    title = models.CharField(max_length=40)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    due_date = models.DateTimeField()
    category = models.CharField(max_length=20)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    
    
    objects = TaskManager()
    
    
    def __str__(self):
      return f'{self.title} assigned to {self.assigned_to.username}'
    
    def get_formatted_due_date(self):
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        
        if self.due_date.date() == now.date():
            return self.due_date.strftime("%I:%M %p")  # Return time alone if due today
        elif self.due_date.date() == tomorrow.date():
            return "Tomorrow"  # Return "Tomorrow" if due tomorrow
        else:
            return self.due_date.strftime("%Y/%m/%d")  # Return full date for other days
