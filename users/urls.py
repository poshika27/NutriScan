from django.urls import path
from . import views
from .views import leftover_view
from .views import cravings_view
from .views import bmi_view
from .views import extract_text,recipe

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('leftover/', leftover_view, name='leftover'),
    path('recipe/', recipe, name='recipe'),
    path('cravings/', cravings_view, name='cravings'),
    path('bmi/', bmi_view, name='bmi'),
    path('logout/', views.user_logout, name='logout'),
    path("extract_text/", extract_text, name="extract_text"),
]
