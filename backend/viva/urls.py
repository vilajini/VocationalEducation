from django.urls import path
from . import views

urlpatterns = [
    path('generate-question/', views.generate_question, name='generate_question'),
    path('submit-answer/', views.submit_answer, name='submit_answer'),

]