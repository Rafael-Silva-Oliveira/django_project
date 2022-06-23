# from django.contrib import admin
# from .models import Student  # new
# # Register your models here.
# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'rollno', 'name', 'email']


from django.contrib import admin
from .models import a_student  # new
# Register your models here.
@admin.register(a_student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id','gender','age','year','area']