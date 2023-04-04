from django.urls import path
from . import views

urlpatterns = [
   path('register/', views.UserRegisterAPI.as_view()),
   path('login/', views.LoginAPIView.as_view()),
   path('dashboard/', views.DashboardAPIView.as_view()),
   

]
