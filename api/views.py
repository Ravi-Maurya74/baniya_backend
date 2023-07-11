from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.db.models import Q
from .models import Student,Transaction,Category,CategoryBudget,Comment,CommunityPost
from .serializers import StudentSerializer, TransactionSerializer, CreateTransactionSerializer,CreateStudentSerializer,CreateCommunityPostSerializer,CommunityPostSerializer,CommentSerializer,CreateCommentSerializer
import datetime
import calendar
from datetime import date, timedelta

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

class StudentCreateView(generics.CreateAPIView):
    queryset=Student.objects.all()
    serializer_class = CreateStudentSerializer

class StudentRetrieveView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'email'

class StudentUpdateView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = CreateTransactionSerializer


class TransactionDeleteView(generics.DestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionUpdateView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class CommunityPostCreateView(generics.CreateAPIView):
    queryset = CommunityPost.objects.all()
    serializer_class = CreateCommunityPostSerializer

class CommunityPostListView(generics.ListAPIView):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        student_id = self.kwargs['student_id']
        context['student_id'] = student_id
        return context
    
class LikeCommunityPostView(generics.UpdateAPIView):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer

    def update(self, request, *args, **kwargs):
        communityPost = self.get_object()
        student_id = request.data['student_id']
        student = Student.objects.get(pk=student_id)
        if communityPost.liked_by.filter(id=student.id).exists():
            communityPost.liked_by.remove(student)
            communityPost.upvotes-=1
        else:
            communityPost.liked_by.add(student)
            communityPost.upvotes+=1
        communityPost.save()
        return super().update(request, *args, **kwargs)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        student_id = self.request.data['student_id']
        context['student_id'] = student_id
        return context
    
class BookmarkCommunityPostView(generics.UpdateAPIView):
    queryset = CommunityPost.objects.all()
    serializer_class = CommunityPostSerializer

    def update(self, request, *args, **kwargs):
        communityPost = self.get_object()
        student_id = request.data['student_id']
        student = Student.objects.get(pk=student_id)
        if communityPost.bookmarked_by.filter(id=student.id).exists():
            communityPost.bookmarked_by.remove(student)
        else:
            communityPost.bookmarked_by.add(student)
        communityPost.save()
        return super().update(request, *args, **kwargs)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        student_id = self.request.data['student_id']
        context['student_id'] = student_id
        return context
    
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        student_id = self.kwargs['student_id']
        context['student_id'] = student_id
        return context
    
class LikeCommentView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        student_id = request.data['student_id']
        student = Student.objects.get(pk=student_id)
        if comment.liked_by.filter(id=student.id).exists():
            comment.liked_by.remove(student)
        else:
            comment.liked_by.add(student)
        comment.save()
        return super().update(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        student_id = self.request.data['student_id']
        context['student_id'] = student_id
        return context
    
@api_view(['GET'])
def monthlyExpenses(request,student_id):

    today = date.today()
    current_year = today.year
    current_month = today.month

    num_days = calendar.monthrange(current_year, current_month)[1]
    first_day = date(current_year, current_month, 1)
    last_day = date(current_year, current_month, num_days)
    response = {}


    current_date = first_day
    while current_date <= last_day:
        if not str(current_date) in response:
            response[str(current_date)] = 0.00
        current_date += timedelta(days=1)


    student = Student.objects.get(pk=student_id)
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    for transaction in student.transactions.filter(Q(date__month=current_month) & Q(date__year=current_year)):
        response[str(transaction.date)]+=float(transaction.amount)
        
    return Response(response,status=200)


    


