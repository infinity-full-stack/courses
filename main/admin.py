from django.contrib import admin
from django.db.models import TextField
from django.forms import Textarea
from django.utils.safestring import mark_safe

from .models import Course, Student, CourseLike, Comment

admin.site.site_header = "EduHub"
admin.site.site_title = "eduhub"
admin.site.login_template = "admin/my_login.html"
admin.site.logout_template = "admin/logout.html"


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("user",)

    formfield_overrides = {
        TextField: {
            "widget": Textarea(attrs={
                "rows": 2,
                "cols": 40,
            })
        },
    }

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk and not instance.user:
                instance.user = request.user
            instance.save()
        formset.save_m2m()


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'price', 'created', 'get_image')
    list_display_links = ('name',)
    list_filter = ('created',)
    list_editable = ('price',)
    search_fields = ('name', 'description')
    fieldsets = [
        (
            "Asosiy",
            {
                'fields': ['name', 'description'],
            }
        ),
        (
            "Media",
            {
                "fields": ["image"],
                "classes": ["collapse"],
                "description": "Bu yerda kurs rasmi bo'ladi!"
            }
        ),
        (
            "Qo'shimcha",
            {
                "fields": ['duration', 'price'],
                "classes": ["collapse"]
            }
        )
    ]
    inlines = [CommentInline]

    @admin.display(description="Rasmi")
    def get_image(self, course):
        if course.image:
            return mark_safe(f'<img src="{course.image.url}" width="100px">')
        return '-'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'courses_count')
    search_fields = ('first_name', 'last_name', 'email')

    @admin.display(description="Kurslar soni")
    def courses_count(self, obj):
        return obj.courses.count()


@admin.register(CourseLike)
class CourseLikeAdmin(admin.ModelAdmin):
    list_display = ('course', 'user')
