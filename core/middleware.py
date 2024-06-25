# middleware.py
from django.http import JsonResponse
from rest_framework import status

class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == status.HTTP_403_FORBIDDEN and not request.user.is_authenticated:
           response.status_code = status.HTTP_401_UNAUTHORIZED
        return response
