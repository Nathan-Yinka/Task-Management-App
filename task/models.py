from django.db import models
from django.db.models import Case,When,IntegerField
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

User = get_user_model()

class TaskQuerySet(models.QuerySet):
  
    def search(self, query=None, status=None, priority=None, due_date=None, category=None):
        filters = {}
        
        if query:
            filters['title__icontains'] = query
        
        if status:
            filters['status__iexact'] = status
        
        if priority:
            filters['priority__iexact'] = priority
        
        if due_date:
            filters['due_date__date'] = due_date
        
        if category:
            filters['category__icontains'] = category
        
        return self.filter(**filters)

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
      
    def search(self, query=None, status=None, priority=None, due_date=None, category=None):
      return self.get_queryset().search(query=query, status=status, priority=priority, due_date=due_date, category=category)


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
      
      
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    due_date = models.DateTimeField()
    category = models.CharField(max_length=100)
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
