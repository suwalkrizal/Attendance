from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Teacher(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = '"attend"."teacher"'
    
class Room(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="rooms")
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = '"attend"."room"'
    
class Student(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="students")
    name = models.CharField(max_length=50)
    face_encoding = models.BinaryField()

    class Meta:
        db_table = '"attend"."student"'

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField(default=timezone.now)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = '"attend"."attendance"'
