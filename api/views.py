from rest_framework.views import APIView
from django.http import JsonResponse
import json
from rest_framework import status as api_response_status

class HealthCheck(APIView):

    def get(self, request, format=None):

        return JsonResponse({
            'success': True,
            'userMessage': 'ok',
            'data': '',
        }, status = api_response_status.HTTP_200_OK)