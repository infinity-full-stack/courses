from django.urls import path
from .views import all_courses, course_detail, all_students, student_detail, create_like

urlpatterns = [
    path('', all_courses, name='all_courses'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('students/', all_students, name='all_students'),
    path('student/<int:student_id>/', student_detail, name='student_detail'),
    path('add/bookmark/<int:course_id>/', create_like, name='create_like'),
]
