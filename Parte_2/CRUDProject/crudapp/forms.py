# from django import forms
# from .models import Student
# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ['id', 'rollno', 'name', 'email']

from django import forms
from .models import a_student
class StudentForm(forms.ModelForm):
    class Meta:
        model = a_student
        fields = ['student_id','gender','age','year','area']
