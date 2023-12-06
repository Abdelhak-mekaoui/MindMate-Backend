from django.db import models
from accounts.models import Patient  

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class Medication(models.Model):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    instructions = models.TextField(blank=True, null=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medications')
    def __str__(self):
        return self.name
    


class MedicationReminder(models.Model):
    STATUS_CHOICES = (
        (-1, 'Pending'),
        (1, 'Completed'),
        (0, 'Not Completed'),
    )

    status = models.IntegerField(choices=STATUS_CHOICES)
    description = models.TextField()
    date = models.DateTimeField()
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medication_reminders')

    def __str__(self):
        return f"Medication reminder for {self.patient.first_name} {self.patient.last_name}"