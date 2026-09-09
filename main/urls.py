from django.urls import path
from main import views



urlpatterns = [
    
    path("",views.home,name="home"),
    path("about/",views.about,name="about"),
    path("contact/",views.contact,name="contact"),
    path("tests/",views.data_view,name="tests"),
    path("tables/",views.table,name="table"),
    path("delete/<int:pk>",views.delete_student,name="delete_student"),
    path("update/<int:pk>",views.update_students,name="update_students"),
    path("portfolio",views.portfolio,name="portfolio"),
    path("details/<int:student_id>",views.details_student,name="details_student"),
    path("register/",views.register,name="register"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("admindashboard/",views.admin_dashboard,name="admindashboard"),
    path(
        "toggle-user-active/<int:user_id>/",
        views.toggle_user_active,
        name="toggle_user_active"
    ),
    path("todolist/", views.to_do_list_view, name="todolist"),
    path("add-task/", views.add_task, name="add_task"),
    path("task-detail/<int:pk>/", views.task_detail, name="task_detail"),
    path("edit-task/<int:pk>/", views.edit_task, name="edit_task"),
    path("delete-task/<int:pk>/", views.delete_task, name="delete_task"),
    path("toggle-task-completed/<int:pk>/", views.toggle_task_completed, name="toggle_task_completed"),
]