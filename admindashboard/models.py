from django.db import models

class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self):
        return self.full_name
    
class courses(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE
    )
    
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
    
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(
        courses,
        on_delete=models.CASCADE
    )
    
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return self.name
    