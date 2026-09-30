from django.shortcuts import render, redirect, get_object_or_404
from . models import Student, courses, Teacher, Lesson
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

@login_required(login_url="orientlogin")
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
    
    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        return redirect("orientlogin")

    teacher = Teacher.objects.get(id=teacher_id)

    teacher_courses = courses.objects.filter(
        teacher=teacher
    )

    context = {
        "teacher": teacher,
        "courses": teacher_courses
    }

    return render(request, "groups.html", context)
    
def group_detail(request, course_id):

    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        return redirect("orientlogin")

    teacher = get_object_or_404(
        Teacher,
        id=teacher_id
    )

    course = get_object_or_404(
        courses,
        id=course_id,
        teacher=teacher
    )

    students = Student.objects.filter(
        course=course
    )

    lessons = Lesson.objects.filter(
        course=course
    ).order_by("-start_date")

    if request.method == "POST":

        # İmtahan nəticəsini yadda saxla
        if "save_score" in request.POST:

            student_id = request.POST.get("student_id")
            score = request.POST.get("score")

            student = get_object_or_404(
                Student,
                id=student_id,
                course=course
            )

            if score:
                student.score = score
                student.save()

            return redirect(
                "group_detail",
                course_id=course.id
            )

        # Yeni dərs yarat
        if "create_lesson" in request.POST:

            topic = request.POST.get("topic")
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")

            if topic and start_date and end_date:

                Lesson.objects.create(
                    topic=topic,
                    start_date=start_date,
                    end_date=end_date,
                    course=course
                )

            return redirect(
                "group_detail",
                course_id=course.id
            )

    context = {
        "teacher": teacher,
        "course": course,
        "students": students,
        "lessons": lessons
    }
    
    return render(request, "group_detail.html", context)


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




def lesson_detail(request, lesson_id):

    return render(request, "lesson_detail.html")

