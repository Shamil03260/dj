from django.urls import path
from admindashboard import views

urlpatterns = [
    path("",views.home_page,name="homepage"),
    path("profile/", views.profile, name="profile"),
    path("login/", views.login_dashboard, name="orientlogin"),
    ]