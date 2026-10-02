from django.urls import path
from admindashboard import views

urlpatterns = [
    path("",views.home_page,name="homepage"),
    path("profile/", views.profile, name="profile"),
    path("login/", views.login_dashboard, name="orientlogin"),
    path("groups/", views.groups, name="groups"),
    path("groups/<int:course_id>/", views.group_detail, name="group_detail"),
    path( "groups/lesson/<int:lesson_id>/", views.lesson_detail, name="lesson_detail"),
    path("lesson/<int:lesson_id>/", views.lesson_detail, name="lesson_detail"),
    path("groups/<int:course_id>/month/<int:year>/<int:month>/", views.month_lessons, name="month_lessons"),
    ]