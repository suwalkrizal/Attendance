from django.shortcuts import render

# Create your views here.
from rest_framework import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404

from apps.models import (
    Teacher,
    Room,
    Student,
    Attendance,
)
from apps.serializers import(
    RoomSerializer,
    StudentSerializer,
    AttendanceSerializer,
)
from apps.utils import encode_face, match_face


class RoomlistCreateAPIView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomDetailAPIView(APIView):
    def get(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def patch(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentListCreateAPIView(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDetailAPIView(APIView):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def patch(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterFaceAPIView(APIView):
    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        image_file = request.FILES.get('face')
        if not image_file:
            return Response({'error': "Face image required"}, status=status.HTTP_400_BAD_REQUEST)

        encoding = encode_face(image_file)
        if encoding:
            student.face_encoding = encoding
            student.save()
            return Response({"status": "face registered successfully"})
        return Response({"error": "No face detected"}, status=status.HTTP_400_BAD_REQUEST)


class AttendanceListCreateAPIView(APIView):
    def get(self, request):
        attendance_records = Attendance.objects.all()
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarkAttendanceAPIView(APIView):
    def post(self, request):
        student_id = request.data.get('student_id')
        image_file = request.FILES.get('face')

        if not student_id or not image_file:
            return Response({"error": "student_id and face image required"}, status=status.HTTP_400_BAD_REQUEST)
        
        student = get_object_or_404(Student, id=student_id)

        if match_face(image_file, student):
            today = timezone.now().date()
            attendance, created = Attendance.objects.get_or_create(student=student, date=today)

            if not attendance.check_in_time:
                attendance.check_in_time = timezone.now()
            else:
                attendance.check_out_time = timezone.now()
            attendance.save()
            return Response({"status": "attendance marked successfully"})
        return Response({"error": "face not matched"}, status=status.HTTP_400_BAD_REQUEST)