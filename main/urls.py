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
    path("admindashboard/", views.admin_dashboard,name=admindashboard)
    
]