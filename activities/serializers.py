from rest_framework import serializers
from .models import Book,BookTrigger,Game



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  



class BookTriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookTrigger
        fields = '__all__'  

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'  
