from django.contrib.auth.decorators import login_required
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
