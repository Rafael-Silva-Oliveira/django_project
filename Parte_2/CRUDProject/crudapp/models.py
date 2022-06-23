from django.db import models
# Create your models here.
class a_student(models.Model):
    student_id = models.CharField(auto_created=False, primary_key=True, serialize=False, verbose_name='student_id',max_length=100)
    gender = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    year = models.FloatField()
    area = models.CharField(max_length=100)

# from django.db import models
# # Create your models here.
# class Student(models.Model):
#     rollno = models.IntegerField()
#     name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100)