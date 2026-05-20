from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")
    duration = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Davomiyligi (soat)")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Narxi")
    image = models.ImageField(upload_to='main/images/', null=True, blank=True, verbose_name="Rasmi")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurslar'
        ordering = ['-created']


class Student(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ismi")
    last_name = models.CharField(max_length=100, verbose_name="Familiyasi")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Telefon")
    courses = models.ManyToManyField(Course, blank=True, verbose_name="Kurslar")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Talaba'
        verbose_name_plural = 'Talabalar'


class CourseLike(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Kurs")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")

    def __str__(self):
        return self.course.name

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likelar'
