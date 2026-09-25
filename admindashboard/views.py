from django.shortcuts import render, redirect
from . models import Student, courses, Teacher
from django.contrib.auth import authenticate, login

def home_page(request):
    teacher_id = request.session.get("teacher_id")
    
    if not teacher_id:
        return redirect("orientlogin")
    
    teacher = Teacher.objects.get(id=teacher_id)
    
    context = {
        "teacher":teacher
        
    }
    
    return render(request,"home_page.html", context)

def profile(request):
    
    teacher_id = request.session.get("teacher_id")
    
    if not teacher_id:
        
        return redirect("orientlogin")
    
    teacher = Teacher.objects.get(id=teacher_id)
    
    context = {
        "teacher":teacher
    }
    
    return render(request, "profile.html", context)


def groups(request):
    
    return render(request, "groups.html")


def login_dashboard(request):

    if request.method == "POST":

        full_name = request.POST.get("username")
        password = request.POST.get("password")

        teacher = Teacher.objects.filter(
            full_name=full_name,
            password=password
        ).first()

        if teacher:
            request.session["teacher_id"] = teacher.id
            request.session["teacher_name"] = teacher.full_name

            return redirect("homepage")

        else:

            return render(request, "orient_login.html", {
                "error": "İstifadəçi adı və ya parol yanlışdır."
            })

    return render(request, "orient_login.html")
