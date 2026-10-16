from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, courses, Teacher, Lesson, LessonAttendance
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.utils import timezone



# @login_required(login_url="orientlogin")
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

    return render(request, "home_page.html", context)


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

    return render(request, "profile.html", context)


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

    lesson_error = None
    score_error = None

    # İmtahan balını yadda saxlamaq
    if request.method == "POST" and "save_score" in request.POST:
        student_id = request.POST.get("student_id")
        exam_score = request.POST.get("exam_score")

        try:
            exam_score = int(exam_score)

            if not 0 <= exam_score <= 100:
                score_error = "Bal 0 ilə 100 arasında olmalıdır."

            else:
                student = get_object_or_404(
                    Student,
                    id=student_id,
                    course=course
                )

                student.exam_score = exam_score
                student.save()

                return redirect(
                    "group_detail",
                    course_id=course.id
                )

        except (ValueError, TypeError):
            score_error = "Düzgün bal daxil et."

    # Yeni dərs yaratmaq
    elif request.method == "POST" and "topic" in request.POST:
        topic = request.POST.get("topic", "").strip()

        start_date = parse_datetime(
            request.POST.get("start_date", "")
        )

        end_date = parse_datetime(
            request.POST.get("end_date", "")
        )

        if not topic or not start_date or not end_date:
            lesson_error = (
                "Bütün dərs məlumatlarını düzgün daxil et."
            )

        elif end_date < start_date:
            lesson_error = (
                "Bitmə tarixi başlama tarixindən əvvəl ola bilməz."
            )

        else:
            if timezone.is_naive(start_date):
                start_date = timezone.make_aware(
                    start_date,
                    timezone.get_current_timezone()
                )

            if timezone.is_naive(end_date):
                end_date = timezone.make_aware(
                    end_date,
                    timezone.get_current_timezone()
                )

            Lesson.objects.create(
                course=course,
                topic=topic,
                start_date=start_date,
                end_date=end_date
            )

            return redirect(
                "group_detail",
                course_id=course.id
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
        "lessons": lessons,
        "lesson_error": lesson_error,
        "score_error": score_error,
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

            return render(
                request,
                "orient_login.html",
                {
                    "error": "İstifadəçi adı və ya parol yanlışdır."
                }
            )

    return render(request, "orient_login.html")


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

    return render(request, "month_lessons.html", context)


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

        return redirect("lesson_detail", lesson_id=lesson.id)

    attendance = LessonAttendance.objects.filter(
        lesson=lesson
    )

    attendance_dict = {}

    for item in attendance:

        attendance_dict[item.student_id] = item.is_present

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

    return render(request, "lesson_detail.html", context)


def contact_us(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        send_mail(
            f"Contact Us - {name}",
            f"Name: {name}\nEmail: {email}\nMessage: {message}",
            settings.EMAIL_HOST_USER,
            ["shamilshirinof@gmail.com"],
        )

    return render(request, "contact_us.html")


def edit_monthlesson(request, lesson_id):
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

    if request.method == "POST":
        topic = request.POST.get("topic", "").strip()
        start_date = parse_datetime(
            request.POST.get("start_date", "")
        )
        end_date = parse_datetime(
            request.POST.get("end_date", "")
        )

        if (
            topic
            and start_date
            and end_date
            and end_date >= start_date
        ):
            lesson.topic = topic
            lesson.start_date = start_date
            lesson.end_date = end_date
            lesson.save()

            return redirect(
                "month_lessons",
                course_id=lesson.course_id,
                year=lesson.start_date.year,
                month=lesson.start_date.month
            )

        context = {
            "lesson": lesson,
            "error": "Məlumatları düzgün daxil et. Bitmə tarixi başlama tarixindən əvvəl ola bilməz."
        }

        return render(
            request,
            "edit_monthlesson.html",
            context
        )

    return render(
        request,
        "edit_monthlesson.html",
        {"lesson": lesson}
    )
    
    
def delete_monthlesson(request, lesson_id):
    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        return redirect("orientlogin")

    teacher = get_object_or_404(Teacher, id=teacher_id)

    lesson = get_object_or_404(
        Lesson,
        id=lesson_id,
        course__teacher=teacher
    )

    if request.method == "POST":
        course_id = lesson.course_id
        year = lesson.start_date.year
        month = lesson.start_date.month

        lesson.delete()

        return redirect(
            "month_lessons",
            course_id=course_id,
            year=year,
            month=month
        )

    return redirect(
        "month_lessons",
        course_id=lesson.course_id,
        year=lesson.start_date.year,
        month=lesson.start_date.month
    )
    
