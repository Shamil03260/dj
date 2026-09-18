from django.contrib import admin
from .models import Student, Author, Book

admin.site.register(Student)
admin.site.register(Author)
admin.site.register(Book)