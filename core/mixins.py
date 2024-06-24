from datetime import datetime

from rest_framework.exceptions import ValidationError

from task.models import Task
from .utils import DateValidationUtility


class TaskQueryMixin:
    
    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        status = self.request.query_params.get('status', None)
        priority = self.request.query_params.get('priority', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        category = self.request.query_params.get('category', None)
        
        errors = []
        
        # Validate status parameter against choices case-insensitively
        if status:
            status_choices = {key.lower(): value for key, value in dict(Task.STATUS_CHOICES).items()}
            if status.lower() not in status_choices:
                errors.append(f"Invalid status '{status}'. Valid choices are {', '.join(status_choices.values())}.")
                
        if priority:
            priority_choices = {key.lower(): value for key, value in dict(Task.PRIORITY_CHOICES).items()}
            if priority.lower() not in priority_choices:
                errors.append(f"Invalid priority '{priority}'. Valid choices are {', '.join(priority_choices.values())}.")
             
        # Validate and parse start_date and end_date using DateValidationUtility   
        start_date, end_date, date_errors = DateValidationUtility.validate_dates(start_date, end_date)
        errors.extend(date_errors)
    
        if errors:
            raise ValidationError(errors)


        qs = super().get_queryset().search(query=query, status=status, priority=priority, start_date=start_date, 
            end_date=end_date, category=category)
        return qs