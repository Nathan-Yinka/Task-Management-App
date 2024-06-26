from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

from task.models import Task
from django.contrib.auth.models import User
from task.form import SignUpForm, LoginForm 
from django.test import TestCase, Client

class TaskListViewTest(TestCase):  
  
    def setUp(self):  
        # Create a user  
        self.user = User.objects.create_user(username='testuser', password='testpass123')  
        self.client.login(username='testuser', password='testpass123')  
  
        # Create tasks with different statuses to match STATUS_CHOICES  
        # Note: Add appropriate values for 'due_date' to test overdue, in progress, and completed tasks  
        Task.objects.create(title="Completed Task", description="Task 1", status="Completed", priority="High", due_date=timezone.now() - timezone.timedelta(days=1), category="Work", assigned_to=self.user)  
        Task.objects.create(title="In Progress Task", description="Task 2", status="In Progress", priority="Medium", due_date=timezone.now() + timezone.timedelta(days=1), category="Home", assigned_to=self.user)  
        Task.objects.create(title="Overdue Task", description="Task 3", status="Overdue", priority="Low", due_date=timezone.now() - timezone.timedelta(days=2), category="Work", assigned_to=self.user)  
  
    def test_context_data(self):  
        response = self.client.get(reverse('home'))  
  
        # Test the context data  
        self.assertTrue('completed_tasks' in response.context)  
        self.assertTrue('in_progress_tasks' in response.context)  
        self.assertTrue('overdue_tasks' in response.context)  
        self.assertTrue('categories' in response.context)  
        self.assertTrue('users' in response.context)  
  
        # Test the correctness of context data  
        self.assertEqual(len(response.context['completed_tasks']), 1)  
        self.assertEqual(len(response.context['in_progress_tasks']), 1)  
        self.assertEqual(len(response.context['overdue_tasks']), 1)  
        self.assertEqual(len(response.context['categories']), 2)
        self.assertEqual(len(response.context['users']), User.objects.count() - 1)  # Exclude the logged-in user  


    def test_get_all_tasks(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_filter_by_status(self):
        response = self.client.get('/api/', {'status': 'Completed'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Completed Task')

    def test_invalid_status(self):
        response = self.client.get('/api/', {'status': 'InvalidStatus'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid status', str(response.data))

    def test_filter_by_priority(self):
        response = self.client.get('/api/', {'priority': 'High'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Completed Task')

    def test_invalid_priority(self):
        response = self.client.get('/api/', {'priority': 'InvalidPriority'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid priority', str(response.data))

    def test_filter_by_dates(self):
        start_date = (timezone.now() - timezone.timedelta(days=2)).strftime('%m/%d/%Y')
        end_date = (timezone.now() + timezone.timedelta(days=2)).strftime('%m/%d/%Y')
        response = self.client.get('/api/', {'start_date': start_date, 'end_date': end_date})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_invalid_dates(self):
        response = self.client.get('/api/', {'start_date': 'invalid', 'end_date': 'invalid'})
        self.assertEqual(response.status_code, 400)

    def test_sort_by_title(self):
        response = self.client.get('/api/', {'sort_by': 'title'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], 'Completed Task')

    def test_invalid_sort_by(self):
        response = self.client.get('/api/', {'sort_by': 'invalid_field'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid sort_by field', str(response.data))
        
        
class TaskRetrieveUpdateDeleteApiViewTests(TestCase):


    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='otherpass123')
        self.client.login(username='testuser', password='testpass123')

        self.task1 = Task.objects.create(title="Task 1", description="Task 1 description", status="In Progress", priority="High", due_date=timezone.now() + timezone.timedelta(days=1), category="Work", assigned_to=self.user)
        self.task2 = Task.objects.create(title="Task 2", description="Task 2 description", status="Completed", priority="Medium", due_date=timezone.now() - timezone.timedelta(days=1), category="Home", assigned_to=self.other_user)

        self.retrieve_url = f'/api/{self.task1.id}/'
        self.update_url = f'/api/{self.task1.id}/'
        self.delete_url = f'/api/{self.task1.id}/'

    def test_retrieve_task(self):
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task1.title)

    def test_update_task(self):
        updated_data = {
            'title': 'Updated Task 1',
            'description': 'Updated description',
            'status': 'Completed',
            'priority': 'Low',
            'due_date': (timezone.now() + timezone.timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'category': 'Work',
            'assigned_to': self.user.id
        }
        response = self.client.put(self.update_url, updated_data, format='json')
        
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, updated_data['title'])
        self.assertEqual(self.task1.description, updated_data['description'])

    def test_update_task_by_non_owner(self):
        self.client.logout()
        self.client.login(username='otheruser', password='otherpass123')
        updated_data = {
            'title': 'Updated Task 1 by non-owner',
            'description': 'Updated description',
            'status': 'Completed',
            'priority': 'Low',
            'due_date': (timezone.now() + timezone.timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'category': 'Work',
            'assigned_to': self.user.id
        }
        response = self.client.put(self.update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_task(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

    def test_delete_task_by_non_owner(self):
        self.client.logout()
        self.client.login(username='otheruser', password='otherpass123')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Task.objects.filter(id=self.task1.id).exists())



class AuthViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('auth') 
        self.home_url = reverse('home')
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_authenticated_user_redirect(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.home_url)

    def test_get_login_form(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/auth.html')
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_get_signup_form(self):
        response = self.client.get(f"{self.login_url}?type=signup")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/auth.html')
        self.assertIsInstance(response.context['form'], SignUpForm)

    def test_login_form_submission(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertRedirects(response, self.home_url)

    def test_signup_form_submission(self):
        signup_data = {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        }
        response = self.client.post(f"{self.login_url}?type=signup", signup_data)
        self.assertRedirects(response, self.home_url)
        self.assertTrue(User.objects.filter(username='newuser').exists())


from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from .models import Task

User = get_user_model()

class TaskModelTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        # Create tasks with different statuses and due dates
        self.task1 = Task.objects.create(
            title="Completed Task",
            description="Task 1",
            status="Completed",
            priority="High",
            due_date=timezone.now() - timedelta(days=1),
            category="Work",
            assigned_to=self.user
        )
        self.task2 = Task.objects.create(
            title="In Progress Task",
            description="Task 2",
            status="In Progress",
            priority="Medium",
            due_date=timezone.now() + timedelta(days=1),
            category="Home",
            assigned_to=self.user
        )
        self.task3 = Task.objects.create(
            title="Overdue Task",
            description="Task 3",
            status="Overdue",
            priority="Low",
            due_date=timezone.now() - timedelta(days=2),
            category="Work",
            assigned_to=self.user
        )

    def test_task_creation(self):
        # Test if tasks are created correctly
        self.assertEqual(Task.objects.count(), 3)
        self.assertEqual(self.task1.title, "Completed Task")
        self.assertEqual(self.task2.status, "In Progress")
        self.assertEqual(self.task3.priority, "Low")


    def test_get_formatted_due_date_tomorrow(self):
        # Test get_formatted_due_date method for tasks due tomorrow
        formatted_date = self.task2.get_formatted_due_date()
        self.assertEqual(formatted_date, "Tomorrow")

    def test_get_formatted_due_date_future(self):
        # Test get_formatted_due_date method for tasks due in the future
        formatted_date = self.task3.get_formatted_due_date()
        self.assertIn("/", formatted_date)  # Check if date format is present

    def test_task_manager_methods(self):
        # Test custom queryset methods of TaskManager
        self.assertEqual(Task.objects.completed().count(), 1)
        self.assertEqual(Task.objects.in_progress().count(), 1)
        self.assertEqual(Task.objects.overdue().count(), 1)
        self.assertEqual(Task.objects.order_by_priority().first(), self.task1)
