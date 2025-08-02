from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('agents', views.AgentViewset, basename='agent')

router2 = DefaultRouter()
router2.register('associates', views.AssociateViewset, basename='associate')

urlpatterns = [
    path('students/', views.studentsView),
    path('student/<int:pk>/', views.studentDetailView),

    path('employees/', views.Employees.as_view()), # telling the path to treat the Employee class as a view
    path('employees/<int:pk>/', views.EmployeeDetail.as_view()),

    # Using mixins - Redone Employee using mixins
    path('staffs/', views.Staffs.as_view()),
    path('staffs/<int:pk>/', views.StaffDetails.as_view()),

    # Using Generics - Redone Employee using Generics
    path('workers/', views.Workers.as_view()),
    path('workers/<int:pk>/', views.WorkerDetails.as_view()),

    # using Viewset
    path('', include(router.urls)),

    # Using ModelViewset
    path('', include(router2.urls)),

    # For blogs app
    path('blogs/', views.BlogsView.as_view()),
    path('comments/', views.CommentsView.as_view()),

    path('blogs/<int:pk>/', views.BlogDetailView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()),
]