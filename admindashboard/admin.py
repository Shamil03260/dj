from django.contrib import admin

from .models import Student, Teacher, courses, Lesson, LessonAttendance

admin.site.register(Teacher)
admin.site.register(courses)
admin.site.register(Student)
admin.site.register(Lesson)
admin.site.register(LessonAttendance)