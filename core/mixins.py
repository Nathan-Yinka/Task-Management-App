from rest_framework.exceptions import ValidationError
from task.models import Task

class TaskQueryMixin:
    
    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        status = self.request.query_params.get('status', None)
        priority = self.request.query_params.get('priority', None)
        due_date = self.request.query_params.get('due_date', None)
        category = self.request.query_params.get('category', None)
        
        # Validate status parameter against choices case-insensitively
        if status:
            status_choices = {key.lower(): value for key, value in dict(Task.STATUS_CHOICES).items()}
            if status.lower() not in status_choices:
                raise ValidationError(f"Invalid status '{status}'. Valid choices are {', '.join(status_choices.values())}.")
            
        if priority:
            priority_choices = {key.lower(): value for key, value in dict(Task.PRIORITY_CHOICES).items()}
            if priority.lower() not in priority_choices:
                raise ValidationError(f"Invalid priority '{priority}'. Valid choices are {', '.join(priority_choices.values())}.")

        qs = super().get_queryset().search(query=query, status=status, priority=priority, due_date=due_date, category=category)
        return qs