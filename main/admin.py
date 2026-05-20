from django.contrib import admin
from .models import Course, Student, CourseLike

admin.site.register([Course, Student, CourseLike])
