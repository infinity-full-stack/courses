from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import Course, Student, CourseLike


def all_courses(request):
    courses = Course.objects.all()
    if request.user.is_authenticated:
        for course in courses:
            if CourseLike.objects.filter(course=course, user=request.user).exists():
                course.like = True
            else:
                course.like = False
    context = {
        'courses': courses
    }
    return render(request, 'main/all_courses.html', context)


def course_detail(request, course_id):
    course = Course.objects.get(pk=course_id)
    students = course.student_set.all()
    return render(request, 'main/course_detail.html', {'course': course, 'students': students})


def all_students(request):
    students = Student.objects.all()
    return render(request, 'main/all_students.html', {'students': students})


def student_detail(request, student_id):
    student = Student.objects.get(pk=student_id)
    return render(request, 'main/student_detail.html', {'student': student})


@login_required(login_url='all_courses')
def create_like(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    like, created = CourseLike.objects.get_or_create(course=course, user=request.user)
    if not created:
        like.delete()
    return redirect('all_courses')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('all_courses')
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}! Ro'yxatdan o'tdingiz.")
            return redirect('all_courses')
        else:
            messages.error(request, "Ro'yxatdan o'tishda xatolik. Qayta urinib ko'ring.")
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('all_courses')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}!")
            return redirect('all_courses')
        else:
            messages.error(request, "Login yoki parol noto'g'ri.")
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, "Siz tizimdan chiqdingiz.")
        return redirect('all_courses')
    return redirect('all_courses')
