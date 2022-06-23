from django.urls import path
from .import views
urlpatterns = [
    path('', views.addStudent, name="add_student"),
    path('update/<id>/', views.edit, name="edit"),
    path('delete/<id>/', views.deleteStudent, name="delete_student"),
]