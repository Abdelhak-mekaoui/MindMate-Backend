from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Patient

User = get_user_model()

class Book(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='book_medications')  # Change related_name

    def __str__(self):
        return self.name

class BookTrigger(models.Model):
    STATUS_CHOICES = (
        (-1, 'Pending'),
        (1, 'Reading'),
        (0, 'Completed'),
    )
    
    status = models.IntegerField(choices=STATUS_CHOICES)
    description = models.TextField()
    date = models.DateTimeField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='triggers')  # Change related_name
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='book_triggers')  # Change related_name

    def __str__(self):
        return f"Trigger for {self.patient.get_full_name()} - Book: {self.book.name}"

class Game(models.Model):
    GAME_CHOICES = (
        (1, 'Game 1'),
        (2, 'Game 2'),
        (3, 'Game 3'),
    )
    STATUS_CHOICES = (
        (-1, 'Not Played'),
        (1, 'Played'),
        (0, 'Pending'),
    )
    name = models.CharField(max_length=255)
    status = models.IntegerField(choices=STATUS_CHOICES)
    score = models.PositiveIntegerField(blank=True, null=True )
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='games_played')  # Change related_name

    def __str__(self):
        return f"Game: {self.name} - Patient: {self.patient.get_full_name()} - Score: {self.score}"
