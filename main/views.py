from django.shortcuts import render , redirect, get_object_or_404
from django.http import HttpResponse
from . models import Student, Tasks
from django.db.models import Q
from django.db.models import F
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

def admin_dashboard(request):
    users = User.objects.all()

    total_users = users.count()
    active_users = users.filter(is_active=True).count()

    context = {
        "users": users,
        "total_users": total_users,
        "active_users": active_users,
    }

    return render(request, "admin_dashboard.html", context)

def toggle_user_active(request, user_id):
    if request.method == "POST":
        user = User.objects.get(id=user_id)

        user.is_active = not user.is_active
        user.save()

    return redirect("admindashboard")