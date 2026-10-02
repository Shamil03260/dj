from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("admindashboard", "0004_lessonattendance"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="student",
            options={},
        ),

        migrations.RemoveField(
            model_name="courses",
            name="created_at",
        ),

        migrations.RemoveField(
            model_name="teacher",
            name="password",
        ),

        migrations.AddField(
            model_name="courses",
            name="end_date",
            field=models.DateField(
                blank=True,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name="courses",
            name="start_date",
            field=models.DateField(
                blank=True,
                null=True,
            ),
        ),

        migrations.AddField(
            model_name="student",
            name="exam_score",
            field=models.IntegerField(
                default=0,
            ),
        ),

        migrations.AddField(
            model_name="student",
            name="left_group_date",
            field=models.DateField(
                blank=True,
                null=True,
            ),
        ),

        migrations.AlterField(
            model_name="courses",
            name="teacher",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="courses",
                to="admindashboard.teacher",
            ),
        ),

        migrations.AlterField(
            model_name="lesson",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lessons",
                to="admindashboard.courses",
            ),
        ),

        migrations.AlterField(
            model_name="lesson",
            name="end_date",
            field=models.DateTimeField(),
        ),

        migrations.AlterField(
            model_name="lesson",
            name="start_date",
            field=models.DateTimeField(),
        ),

        migrations.AlterField(
            model_name="lesson",
            name="topic",
            field=models.CharField(
                max_length=255,
            ),
        ),

        migrations.AlterField(
            model_name="lessonattendance",
            name="lesson",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attendance",
                to="admindashboard.lesson",
            ),
        ),

        migrations.AlterField(
            model_name="lessonattendance",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attendance",
                to="admindashboard.student",
            ),
        ),

        migrations.AlterField(
            model_name="student",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="students",
                to="admindashboard.courses",
            ),
        ),
    ]