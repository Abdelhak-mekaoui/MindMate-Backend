from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, BookTrigger, Game
from .serializers import BookSerializer, BookTriggerSerializer, GameSerializer
from accounts.models import Patient

class BookAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = dict(request.data)
        patient_id = data.pop('patient', None)
        patient = None
        if patient_id:
            patient = Patient.objects.filter(id=patient_id).first()

        books = Book.objects.filter(user=request.user, patient=patient)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        data['user'] = request.user.id
        patient_id = data.pop('patient', None)
        
        patient = None
        if patient_id:
            patient = Patient.objects.filter(id=patient_id).first()
            if not patient:
                return Response(
                    {'error': 'Patient with the provided ID does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        data['patient'] = patient.id if patient else None

        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BookTriggerAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = dict(request.data)
        patient_id = data.pop('patient', None)
        patient = None
        if patient_id:
            patient = Patient.objects.filter(id=patient_id).first()

        bookTriggers = BookTrigger.objects.filter(user=request.user, patient=patient)
        serializer = BookTriggerSerializer(bookTriggers, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        data['user'] = request.user.id
        patient_id = data.pop('patient', None)
        
        patient = None
        if patient_id:
            patient = Patient.objects.filter(id=patient_id).first()
            if not patient:
                return Response(
                    {'error': 'Patient with the provided ID does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        data['patient'] = patient.id if patient else None
        
        serializer = BookTriggerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class GameAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = dict(request.data)
        patient_id = data.pop('patient', None)
        patient = None
        if patient_id:
            patient = Patient.objects.filter(id=patient_id).first()

        games = Game.objects.filter(user=request.user, patient=patient)
        serializer = GameSerializer(games, many=True) 
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        data['user'] = request.user.id
        patient_id = data.pop('patient', None)
        
        patient = None
        if patient_id:
            patient = Patient.objects.filter(id=patient_id).first()
            if not patient:
                return Response(
                    {'error': 'Patient with the provided ID does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        data['patient'] = patient.id if patient else None
        
        serializer = GameSerializer(data=data)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
