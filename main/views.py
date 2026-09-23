from django.shortcuts import render , redirect, get_object_or_404
from django.http import HttpResponse
from . models import Student, Tasks, Movie, Author, Book
from django.db.models import Q
from django.db.models import F
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


# User.objects.create_user(username="nasib",email="nasib333@gmail.com",password="123456789").save()

# Student(
# name="ali",
# email="testsd111@gmail.com",
# price = 10
#     ).save()





def home(request):
    
    # student = Student.objects.create(
    # name="Ali",
    # age=20,
    # email="testtt55GMail.com",
    # price=10
    # )
    
    # student.save()

    # SELECT * FROM students;
    student = Student.objects.all()
    # print(request.method)
    # name = "Nasib"
    # surname = "Nasibov"
    
    # students = Student.objects.get(age=20)
    # students = Student.objects.filter(name__icontains="ali")
    # students = Student.objects.exclude(age=70)
    # students = Student.objects.all().order_by("-age")
    students = Student.objects.all().count()
    # student = Student.objects.all().first()
    student = Student.objects.all().last()
    
    number = 10
    
    products = [
    "iPhone",
    "Samsung",
    "Xiaomi"
    ] 
    
    context = {
        "products":products,
        "number":number,
        "student":student,
        "students_count":students
        }
    
    return render(request,"home.html",context)


def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")


def data_view(request):
    return render(request,"data.html")

@login_required(login_url="login")
def table(request):
    
    search_results = ""
    search = request.GET.get("search")
    
    if search:
    
        # search_results = Student.objects.filter(
            
        #     Q(name__icontains=search) | Q(email__icontains=search)
            
            
        #     )
        
        search_results = Student.objects.filter(
                
                ~Q(name__icontains=search)
                
                
               )
    
    
    
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        price = request.POST.get("price")
        age = request.POST.get("age")
        image = request.FILES.get("image")
        
        Student(name=name, email= email,price = price,age = age, image=image).save()
    
    
    student = Student.objects.all()
    
    # larger than
    # x = Student.objects.filter(discount_price__lt=F("price"))
    # for i in x:
    #     print("endirimli qiymeti boyuk olanlar",i.price,i.discount_price,i.name)
    
    # Student.objects.update(
    # price=F("price") + 10
    # )

    
    context = {
        "students":student,
        "search_results":search_results,
        "search":search
    }
    return render(request,"table.html",context)


def details_student(request,student_id):
    
    students = get_object_or_404(Student,id=student_id)
    
    
    
    return render(request,"details.html",{"students":students})


def delete_student(request, pk):
    Student.objects.get(id=pk).delete()
    
    return redirect("table")

def update_students(request, pk):
    student = get_object_or_404(Student,id=pk)
    
    if request.method == "POST":
        student.name = request.POST.get("name")
        student.email = request.POST.get("email")
        student.price = request.POST.get("price")
        student.age = request.POST.get("age")
        student.save()
        
        return redirect("table")

    return render(request,"student_update.html",{"students":student})
    
def portfolio(request):
    
    return render(request,"portfolio.html")

    

  
    
def register(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("pass")
        re_pass = request.POST.get("re_pass")
        
        if password == re_pass:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already exists")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.warning(request,"Email already exists")
                return redirect("register")
            else:
                user = User.objects.create_user(username=username, password=password, 
                                        email=email,)
                user.save()
                return redirect("login")
        else:
            messages.error(request, "Password doesn't match")
            return redirect('register')

    return render(request,"register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("your_name")
        password = request.POST.get("your_pass")
        
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            
            remember_me = request.POST.get("remember_me")
            
            if remember_me:
                    request.session.set_expiry(60 * 60 * 24 * 14)
            else:
                request.session.set_expiry(0)
                
            return redirect("admindashboard")

    return render(request,"login.html")

def logout_view(request):
    
    logout(request)
    
    return redirect("login")


@login_required(login_url="login")
def admin_dashboard(request):
    users = User.objects.all()

    total_users = users.count()
    

    context = {
        "users": users,
        "total_users": total_users
    }

    return render(request, "admin_dashboard.html", context)

def toggle_user_active(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)

        user.is_active = not user.is_active
        user.save()

    return redirect("admindashboard")


def to_do_list_view(request):
    tasks = Tasks.objects.all().order_by("-created_at")

    context = {
        "tasks": tasks
    }
    
    return render(request, "to_do_list.html", context)

def add_task(request):
    if request.method == "POST":
        if request.POST.get('cancel') == 'cancel':
            return redirect("todolist")
        else:
            title = request.POST.get("title")
            description = request.POST.get("description")
        
        

            Tasks.objects.create(
                title=title,
                description=description
            )

            return redirect("todolist")


    return render(request, "add_task.html")

def task_detail(request, pk):
    task = get_object_or_404(Tasks, id=pk)
    
    context = {
        "task": task
    }

    return render(request, "task_detail.html", context)


def edit_task(request, pk):
    task = get_object_or_404(Tasks, id=pk)

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.description = request.POST.get("description")
        task.save()

        return redirect("task_detail", pk=task.id)
    
    context = {
        "task": task
    }

    return render(request, "edit_task.html", context)

def delete_task(request, pk):
    task = get_object_or_404(Tasks, id=pk)

    if request.method == "POST":
        task.delete()
        return redirect("todolist")
    context = {
        "task": task
        
    }
    return render(request, "delete_task.html", context)

def toggle_task_completed(request, pk):
    task = get_object_or_404(Tasks, id=pk)

    task.completed = not task.completed
    task.save()

    return redirect("todolist")

# movies
def movie_list(request):
    movies = Movie.objects.all()

    search = request.GET.get("search")
    genre = request.GET.get("genre")
    year = request.GET.get("year")
    rating = request.GET.get("rating")

    if search:
        movies = movies.filter(title__icontains=search)

    if genre:
        movies = movies.filter(genre__iexact=genre)

    if year:
        movies = movies.filter(year=year)

    if rating:
        movies = movies.filter(rating__gte=rating)

    genres = Movie.objects.values_list("genre", flat=True).distinct()
    years = Movie.objects.values_list("year", flat=True).distinct()

    context = {
        "movies": movies,
        "genres": genres,
        "years": years,
    }

    return render(request, "movie_list.html", context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    context = {
        "movie": movie
    }

    return render(request, "movie_detail.html", context)


def add_movie(request):
    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        year = request.POST.get("year")
        genre = request.POST.get("genre")
        rating = request.POST.get("rating")
        image = request.FILES.get("image")

        Movie.objects.create(
            title=title,
            description=description,
            year=year,
            genre=genre,
            rating=rating,
            image=image
        )

        return redirect("movie_list")

    return render(request, "add_movie.html")


def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":

        movie.title = request.POST.get("title")
        movie.description = request.POST.get("description")
        movie.year = request.POST.get("year")
        movie.genre = request.POST.get("genre")
        movie.rating = request.POST.get("rating")

        if request.FILES.get("image"):
            movie.image = request.FILES.get("image")

        movie.save()

        return redirect("movie_detail", movie_id=movie.id)

    context = {
        "movie": movie
    }
    
    
    return render(request, "edit_movie.html", context)


def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        movie.delete()
        return redirect("movie_list")

    context = {
        "movie": movie
    }
    
    return render(request, "delete_movie.html", context)


# author
def authors(request):
    authors = Author.objects.all()

    context = {
        "authors": authors
    }
    
    return render(request, "authors.html", context)


def author_detail(request, id):
    author = get_object_or_404(Author, id=id)
    

    context = {
        "author": author
    }

    return render(request, "author_detail.html", context)


def books(request):
    books = Book.objects.all()
    
    context = {
        "books": books
    }

    return render(request, "books.html", context)


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)

    context = {
        "book": book
    }
    
    return render(request, "book_detail.html", context)