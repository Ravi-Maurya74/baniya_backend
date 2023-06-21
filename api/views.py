from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.db.models import Q
from .models import Student,Transaction,Category,CategoryBudget
from .serializers import StudentSerializer

class IdentifyStudent(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'email'

@api_view(['POST'])
def addTransaction(request):
    received_json_data = json.loads(request.body)
    title = received_json_data['title']
    amount = received_json_data['amount']
    category = Category.objects.get(pk=received_json_data['category'])
    student = Student.objects.get(pk=received_json_data['student'])
    
    transaction = Transaction(title=title,amount=amount,student=student,category=category)
    transaction.save()

    studentData = Student.objects.get(pk=received_json_data['student'])
    data = StudentSerializer(studentData).data
    return Response(data)

@api_view(['POST'])
def addCategoryBudget(request):
    received_json_data = json.loads(request.body)
    category = Category.objects.get(pk=received_json_data['category'])
    budget = received_json_data['budget']
    student = Student.objects.get(pk=received_json_data['student'])
    categoryBudget = CategoryBudget(category=category,budget=budget,student=student)
    categoryBudget.save()
    studentData = Student.objects.get(pk=received_json_data['student'])
    data = StudentSerializer(studentData).data
    return Response(data)