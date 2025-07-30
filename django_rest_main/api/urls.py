from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.studentsView),
    path('student/<int:pk>/', views.studentDetailView),

    path('employees/', views.Employees.as_view()), # telling the path to treat the Employee class as a view
    path('employees/<int:pk>/', views.EmployeeDetail.as_view()),

    # Using mixins - Redone Employee using mixins
    path('staffs/', views.Staffs.as_view()),
    path('staffs/<int:pk>/', views.StaffDetails.as_view()),
]