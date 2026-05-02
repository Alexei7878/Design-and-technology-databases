from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView
# from django.shortcuts import redirect

from .models import Employee


class UserLoginView(View):
    template_name = "core/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if user is not None:
            login(request, user)
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            return redirect("employees")

        return render(
            request,
            self.template_name,
            {"error": "Неверный логин или пароль"},
        )


class UserRegisterView(View):
    template_name = "core/register.html"
    success_url = reverse_lazy("login")

    def get(self, request):
        return self.render_to_response()

    def post(self, request):
        part1 = ['username', 'password', 'password_chek']
        part2 = ['first_name', 'last_name', 'position', 'department']

        required_fields = part1 + part2

        field_names = {
            'username': "Логин",
            'password': "Пароль",
            'password_chek': 'Подтверждение пароля',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'position': "Должность",
            'department': "Подразделение"
        }

        errors = {}

        for field in required_fields:
            if not request.POST.get(field):
                errors[field] = f"Поле {field_names[field]} обязательно для заполнения!"

        password_chek = request.POST.get("password_chek")
        password = request.POST.get("password")

        if (password != password_chek):
            errors['password_chek'] = "Пароли не совпадают!"

        if errors:
            return render(request, 'core/register.html', {'errors': errors})

        user = User.objects.create_user(
            username=request.POST.get("username"),
            password=request.POST.get("password"),
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
        )

        Employee.objects.create(
            user=user,
            position=request.POST.get("position"),
            department=request.POST.get("department"),
        )

        return redirect(self.success_url)

    def render_to_response(self, **context):
        return TemplateView.as_view(
            template_name=self.template_name,
            extra_context=context,
        )(self.request)


class EmployeeListView(LoginRequiredMixin, ListView):
    model = Employee
    template_name = "core/employees.html"
    context_object_name = "employees"
    login_url = reverse_lazy("login")

    def get_queryset(self):
        return Employee.objects.select_related("user")


class EmployeeProfile(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = "core/profile.html"
    context_object_name = "profile"
    login_url = reverse_lazy("login")

    def get_object(self, queryset=None):
        return Employee.objects.select_related("user").get(user=self.request.user)


"""class LogoutConfirmView(TemplateView):
    template_name = 'logout_confirm.html'"""


class Log_out(View):
    def get(self, request, *args, **kwargs):
        return redirect('login')
