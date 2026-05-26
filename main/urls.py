from django.urls import path
from .views import (all_courses, course_detail, all_students, student_detail,
                    create_like, register_view, login_view, logout_view)

urlpatterns = [
    path('', all_courses, name='all_courses'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('students/', all_students, name='all_students'),
    path('student/<int:student_id>/', student_detail, name='student_detail'),
    path('add/bookmark/<int:course_id>/', create_like, name='create_like'),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
