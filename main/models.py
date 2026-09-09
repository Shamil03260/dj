from django.db import models





class Student(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(null=True,blank=True)
    email = models.EmailField(unique=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    discount_price = models.DecimalField(
    max_digits=10,
    decimal_places=2
    )

    image = models.ImageField(upload_to="students/")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name = "Sagird"
        verbose_name_plural = "Sagirdler"
    
    def __str__(self):
        return f'{self.name} | {self.email}'
    
class Tasks(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)