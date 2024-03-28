from api.views import HealthCheck
from django.urls import path

urlpatterns = [
    path('health/', HealthCheck.as_view()),

]