# Task Management System Documentation

## Table of Contents

1. **Introduction**
   - [Project Overview](#project-overview)
   - [Purpose and Goals](#purpose-and-goals)
   - [Technologies Used](#technologies-used)

2. **Setup Instructions**
   - [Prerequisites](#prerequisites)
   - [Installation Steps](#installation-steps)
   - [Configuration](#configuration)

3. **Backend Development**
   - [Django Setup](#django-setup)
   - [Models](#models)
   - [Views and API Endpoints](#views-and-api-endpoints)
   - [User Authentication and Authorization](#user-authentication-and-authorization)

4. **Frontend Development**
   - [HTML Layout](#html-layout)
   - [Styling with TailwindCSS](#styling-with-tailwindcss)
   - [Dynamic Interactions with jQuery](#dynamic-interactions-with-jquery)
   - [Drag-and-Drop Functionality](#drag-and-drop-functionality)

5. **Testing**
   - [Unit Tests for Backend](#unit-tests-for-backend)
   - [Integration Tests](#integration-tests)
   - [Frontend Testing Considerations](#frontend-testing-considerations)

6. **Deployment**
   - [Deployment Steps](#deployment-steps)
   - [Environment Configuration](#environment-configuration)

7. **Additional Features**
   - [Search and Filtering](#search-and-filtering)
   - [Error Handling](#error-handling)


8. **Credits**
    - [Authors](#authors)

---

## 1. Introduction

### Project Overview

The Task Management System is a web application designed to help users manage their tasks efficiently. It provides features for creating, updating, deleting, and tracking tasks based on their status, priority, and due dates.

### Purpose and Goals

The primary goal of this project is to develop a robust task management system that integrates seamlessly with Django for backend functionality and utilizes TailwindCSS and jQuery for frontend design and dynamic interactions.

### Technologies Used

- **Backend:** Django, Django REST Framework
- **Frontend:** HTML, TailwindCSS, jQuery
- **Database:** SQLite (for development), PostgreSQL (for production)
- **Testing:** Django TestCase, Selenium (for frontend testing)
- **Deployment:** Heroku, Docker (optional)

---

## 2. Setup Instructions

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Django
- django restframe work
- Node.js (for TailwindCSS)
- npm (Node Package Manager)

### Installation Steps

1. Clone the repository from GitHub:
```
    git clone https://github.com/Nathan-Yinka/Task-Management-App.git
    cd Task-Management-App
```


2. Set up a virtual environment (optional but recommended):
```
    python -m venv venv
    source venv/bin/activate 

    # On Windows use 

    venv\Scripts\activate
```


3. Install Python dependencies:
```
    pip install -r requirements.txt
```


4. Install frontend dependencies (TailwindCSS):
```
   npm install
```


### Configuration

1. Configure Django settings:
- Set up database settings in `settings.py`.
- Configure static files and media settings.

2. Perform database migrations:
```
    python manage.py makemigrations
    python manage.py migrate
```


3. Create a superuser (for admin access):
```
    python manage.py createsuperuser
```


4. Start the development server:
```
    python manage.py runserver
```

- server is running on localhost:8000
---

## 3. Backend Development

### Django Setup

- Initialize a new Django project.
- Configure settings for databases, static files, and middleware.

### Models

- **Task Model:** Define fields for tasks such as `title`, `description`, `status`, `priority`, `due_date`, `category`, and `assigned_to`.

### Views and API Endpoints

- Create views and API endpoints for CRUD operations on tasks.
- Implement authentication and authorization using Django's built-in functionalities or third-party packages.

### User Authentication and Authorization

- Integrate user authentication mechanisms.
- Ensure proper authorization checks for accessing and modifying tasks.

---

## 4. Frontend Development

### HTML Layout

- Design HTML templates based on the provided design.
- Structure pages for tasks, dashboard, and user interface components.

### Styling with TailwindCSS

- Use TailwindCSS for responsive and modern styling.
- Customize styles for buttons, forms, cards, and task lists.

### Dynamic Interactions with jQuery

- Implement AJAX requests with jQuery to fetch and update tasks dynamically.
- Add functionalities like search, filtering, sorting, and modal dialogs for task operations.

### Drag-and-Drop Functionality

- Enable drag-and-drop interactions to change task statuses (e.g., move tasks from "In Progress" to "Completed").

---

## 5. Testing

### Unit Tests for Backend

- Write unit tests using Django's `TestCase` for models, views, and API endpoints.
- Test CRUD operations, validations, and error handling.

### Integration Tests

- Implement integration tests to ensure proper interaction between frontend and backend components.
- Test scenarios for user actions, form submissions, and API responses.

### Frontend Testing Considerations

- Use tools like Selenium for automated testing of frontend interactions and UI elements.
- Write test cases to validate user flows, error messages, and responsiveness.

---

## 6. Deployment

### Deployment Steps

- Deploy the application to a production server (e.g., Heroku, AWS, DigitalOcean).
- Configure environment variables for sensitive information (e.g., database credentials, API keys).

### Environment Configuration

- Set up static file serving and media storage configurations.
- Ensure security measures such as HTTPS, CSRF protection, and secure authentication practices.

---

## 7. Additional Features

### Search and Filtering

- Implement search functionality to find tasks based on keywords.
- Enable filtering tasks by status, priority, due date range, and category.
- Drag and Drop function
- User Authorization and Authentication
- Sorting Task according to due date,priority
- User can add task by clicking on the add button
- User can delete task by clicking on the delete button
- User can update task by clicking on the update button
- User can update task status via the drag and drop functons
- security system is very good and best pratices was used
- user cannot perform some task with been logged in 

### Error Handling

- Implement robust error handling for invalid inputs, server errors, and API exceptions.
- Provide informative error messages to users for better usability.


---


## 8. Credits

### Authors

- Oludare Nathaniel Adeyinka


