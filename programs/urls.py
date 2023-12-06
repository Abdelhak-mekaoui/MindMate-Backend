from .views import *
from django.urls import path

urlpatterns = [
    path('medications/', MedicationAPI.as_view(), name='medications'),
    path('medication_reminders/', MedicationReminderAPI.as_view(), name='medication_reminder'),
    
]
