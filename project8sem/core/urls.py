from django.urls import path

from .views import EmployeeListView, UserLoginView, UserRegisterView, EmployeeProfile, Log_out

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("employees/", EmployeeListView.as_view(), name="employees"),
    path("profile/", EmployeeProfile.as_view(), name="profile"),
    path("logout/", Log_out.as_view(), name="log_out"),
]
