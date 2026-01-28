from django.contrib import admin
from .models import (
    Teacher,
    Room,
    Student,
    Attendance,
)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username', 'user__email')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'name')
    search_fields = ('teacher__user__username', 'teacher__user__email')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'name')
    search_fields = ('room__teacher__user__username', 'room__teacher__user__email')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'date', 'check_in_time', 'check_out_time')
    search_fields = ('student__room__teacher__user__username', 'student__room__teacher__user__email')
