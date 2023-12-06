from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Medication, MedicationReminder
from .serializers import MedicationSerializer, MedicationReminderSerializer
from accounts.models import Patient  # Import the Patient model from the other microservice
import pika
import json


class MedicationAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = dict(request.data)
        patient_id = data.pop('patient', None)
        patient = None
        if patient_id:
            patient = Patient.objects.filter(id=patient_id).first()

        medications = Medication.objects.filter(user=request.user,patient=patient)
        serializer = MedicationSerializer(medications, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        data = dict(request.data)  # Create a new dictionary with the data
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

        serializer = MedicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class MedicationReminderAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data = dict(request.data)
        patient_id = data.pop('patient', None)
        print(f"this is the patinet id from md rem : {patient_id}")
        patient = None
        patient_id = request.query_params.get('patient', None)

        if patient_id:
            patient = Patient.objects.filter(id=patient_id).first()

        medicationReminders = MedicationReminder.objects.filter(user=request.user,patient=patient)
        serializer = MedicationReminderSerializer(medicationReminders, many=True)
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
        
        serializer = MedicationReminderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            #This part is about to send the message to the server that will inform the robot about the changes of medicationReminder
            # Create a message to send to RabbitMQ
            print("Starting the rabbit mq process...")
            message = {
                'user_id': request.user.id,
                'patient_id': patient.id if patient else None,
                'message_type': 'medication_reminder_created',  # Customize this
                'data': serializer.data
            }

            # Publish the message to RabbitMQ
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  
                channel = connection.channel()
                channel.queue_declare(queue='medication_reminder_queue')  
                channel.basic_publish(exchange='', routing_key='medication_reminder_queue', body=json.dumps(message))
                connection.close()
            except Exception as e:
                print(f"Error sending message to RabbitMQ: {e}")

            print("Finishing rabbit mq process...")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

