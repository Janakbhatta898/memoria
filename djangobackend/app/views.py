from django.shortcuts import render, redirect
from django.http import JsonResponse, StreamingHttpResponse
from .models import Patient, Reminder
from rest_framework import generics
from .serializers import PatientSerializer
from django.utils.timezone import now
from datetime import timedelta
from . import face_recognition
from django.http import JsonResponse
from .models import Todo

def todo_list(request):
    patient_id = request.session.get('patient_id')

    todos = Todo.objects.filter(
        patient_id=patient_id
    ).values("id", "todo")

    return JsonResponse(list(todos), safe=False)  


def home(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id', '').strip()
        if patient_id:
            request.session['patient_id'] = patient_id
            return redirect('camera')
    return render(request, 'app/index.html')


def camera(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('home')
    return render(request, 'app/patient_ar.html', {'patient_id': patient_id})

# Video feed endpoint - streams video with face recognition and reminders
def video_feed(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('home')
    
    return StreamingHttpResponse(
        face_recognition.gen_frames(patient_id),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

# Simple API view for patients
class PatientAPIView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
