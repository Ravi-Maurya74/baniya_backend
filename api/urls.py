from django.urls import path
from api import views

urlpatterns = [
    path('login/<email>',views.IdentifyStudent.as_view()),
    path('addTransaction/',views.addTransaction),
    path('addCategoryBudget/',views.addCategoryBudget),
]