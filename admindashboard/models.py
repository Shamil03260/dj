from django.db import models


class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self):
        return self.full_name


class courses(models.Model):
    name = models.CharField(max_length=100)

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="courses"
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
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
        on_delete=models.CASCADE,
        related_name="students"
    )

    exam_score = models.IntegerField(
        default=0
    )

    # Qrupdan çıxıbsa tarix burada saxlanılır.
    # Aktiv tələbədə NULL qalır.
    left_group_date = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        courses,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    topic = models.CharField(
        max_length=255
    )

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    def __str__(self):
        return self.topic


class LessonAttendance(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="attendance"
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance"
    )

    is_present = models.BooleanField(
        default=False
    )

    class Meta:
        unique_together = (
            "lesson",
            "student"
        )

    def __str__(self):
        return f"{self.student.name} - {self.lesson.topic}"

