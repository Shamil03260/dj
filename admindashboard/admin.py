from django.contrib import admin

from .models import Student, Teacher, courses

admin.site.register(Teacher)
admin.site.register(courses)
admin.site.register(Student)