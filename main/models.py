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
    
    
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    year = models.IntegerField()
    genre = models.CharField(max_length=100)
    rating = models.FloatField()
    image = models.ImageField(upload_to="movies/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
    
# author
class Author(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_date = models.DateField()
    bio = models.TextField()

    def __str__(self):
        return f"{self.name} {self.surname}"


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    published_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"
    )

    def __str__(self):
        return self.title