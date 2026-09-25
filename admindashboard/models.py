from django.db import models

class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name} {self.email}"
    
class courses(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return {self.name}
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(
        courses,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return {self.name}
    
    