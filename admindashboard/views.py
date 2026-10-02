from django.shortcuts import render, redirect, get_object_or_404

from .models import Student, courses, Teacher, Lesson, LessonAttendance

from django.contrib.auth.decorators import login_required


@login_required(login_url="orientlogin")
def home_page(request):

    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        return redirect("orientlogin")

    teacher = get_object_or_404(
        Teacher,
        id=teacher_id
    )

    context = {
        "teacher": teacher
    }

    return render(
        request,
        "home_page.html",
        context
    )


def profile(request):

    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        return redirect("orientlogin")

    teacher = get_object_or_404(
        Teacher,
        id=teacher_id
    )

    context = {
        "teacher": teacher
    }

    return render(
        request,
        "profile.html",
        context
    )


def groups(request):

    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        return redirect("orientlogin")

    teacher = get_object_or_404(
        Teacher,
        id=teacher_id
    )

    group_list = courses.objects.filter(
        teacher=teacher
    )

    context = {
        "teacher": teacher,
        "groups": group_list
    }

    return render(
        request,
        "groups.html",
        context
    )


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
    ).order_by("name")

    lessons = Lesson.objects.filter(
        course=course
    ).order_by("start_date")

    context = {
        "teacher": teacher,
        "course": course,
        "students": students,
        "lessons": lessons
    }

    return render(
        request,
        "group_detail.html",
        context
    )


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

            return render(
                request,
                "orient_login.html",
                {
                    "error": "İstifadəçi adı və ya parol yanlışdır."
                }
            )

    return render(
        request,
        "orient_login.html"
    )


def month_lessons(request, course_id, year, month):

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

    lessons = Lesson.objects.filter(
        course=course,
        start_date__year=year,
        start_date__month=month
    ).order_by("start_date")

    month_names = {
        1: "Yanvar",
        2: "Fevral",
        3: "Mart",
        4: "Aprel",
        5: "May",
        6: "İyun",
        7: "İyul",
        8: "Avqust",
        9: "Sentyabr",
        10: "Oktyabr",
        11: "Noyabr",
        12: "Dekabr"
    }

    context = {
        "teacher": teacher,
        "course": course,
        "lessons": lessons,
        "year": year,
        "month": month,
        "month_name": month_names[month]
    }

    return render(
        request,
        "month_lessons.html",
        context
    )


def lesson_detail(request, lesson_id):

    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        return redirect("orientlogin")

    teacher = get_object_or_404(
        Teacher,
        id=teacher_id
    )

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id,
        course__teacher=teacher
    )

    students = Student.objects.filter(
        course=lesson.course
    ).order_by("name")

    # Davamiyyət göndərilibsə
    if request.method == "POST":

        for student in students:

            checkbox_name = f"student_{student.id}"

            is_present = checkbox_name in request.POST

            LessonAttendance.objects.update_or_create(
                lesson=lesson,
                student=student,
                defaults={
                    "is_present": is_present
                }
            )

        return redirect(
            "lesson_detail",
            lesson_id=lesson.id
        )

    # Mövcud davamiyyət məlumatlarını götürürük
    attendance = LessonAttendance.objects.filter(
        lesson=lesson
    )

    attendance_dict = {}

    for item in attendance:

        attendance_dict[item.student_id] = item.is_present

    # HTML üçün student + davamiyyət məlumatı
    student_rows = []

    for student in students:

        student_rows.append({
            "student": student,
            "is_present": attendance_dict.get(
                student.id,
                False
            )
        })

    context = {
        "teacher": teacher,
        "lesson": lesson,
        "course": lesson.course,
        "student_rows": student_rows
    }

    return render(
        request,
        "lesson_detail.html",
        context
    )

