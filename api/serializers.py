from rest_framework import serializers
from .models import Student,Transaction, Comment,CommunityPost
import json
from django.forms.models import model_to_dict
from django.utils import timezone
import datetime
from django.db.models import Q

class StudentSerializer(serializers.ModelSerializer):
    budgets = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()
    expense = serializers.SerializerMethodField()

    def get_budgets(self, instance):
        result = []
        for budget in instance.budgets.all():
            m = {
                "name": budget.category.name,
                "amount": budget.budget
            }
            result.append(m)
        return result
    
    def get_transactions(self,instance):
        result = []
        for transaction in instance.transactions.all():
            m = {
                "id":transaction.id,
                "title": transaction.title,
                "date": transaction.date,
                "amount": transaction.amount,
                "category": transaction.category.name
            }
            result.append(m)
        return result
    
    def get_expense(self,instance):
        expense = 0
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        for transaction in instance.transactions.filter(Q(date__month=current_month) & Q(date__year=current_year)):
            expense+=transaction.amount
        return expense
    

    class Meta:
        model = Student
        fields = [
            'id',
            'name',
            'email',
            'city',
            'total_budget',
            'credit_score',
            'budgets',
            'transactions',
            'expense',
        ]
        extra_kwargs = {
            'email': {'read_only': True}
        }


class CreateStudentSerializer(serializers.ModelSerializer):
    budgets = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()
    expense = serializers.SerializerMethodField()

    def get_budgets(self, instance):
        result = []
        for budget in instance.budgets.all():
            m = {
                "name": budget.category.name,
                "amount": budget.budget
            }
            result.append(m)
        return result
    
    def get_transactions(self,instance):
        result = []
        for transaction in instance.transactions.all():
            m = {
                "id":transaction.id,
                "title": transaction.title,
                "date": transaction.date,
                "amount": transaction.amount,
                "category": transaction.category.name
            }
            result.append(m)
        return result
    
    def get_expense(self,instance):
        expense = 0
        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year
        for transaction in instance.transactions.filter(Q(date__month=current_month) & Q(date__year=current_year)):
            expense+=transaction.amount
        return expense
    

    class Meta:
        model = Student
        fields = [
            'id',
            'name',
            'email',
            'city',
            'total_budget',
            'credit_score',
            'budgets',
            'transactions',
            'expense',
        ]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'title',
            'amount',
            'date',
        ]

class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id',
            'title',
            'amount',
            'date',
            'student',
            'category',
        ]

class CommunityPostSerializer(serializers.ModelSerializer):

    student = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    bookmarked = serializers.SerializerMethodField()

    def get_student(self,instance):
        return instance.student.name
    
    def get_liked(self,instance):
        student_id = self.context['student_id']
        student_instance = Student.objects.get(pk=student_id)
        return student_instance in instance.liked_by.all()
    
    def get_bookmarked(self,instance):
        student_id = self.context['student_id']
        student_instance = Student.objects.get(pk=student_id)
        return student_instance in instance.bookmarked_by.all()

    class Meta:
        model = CommunityPost
        fields = [
            'id',
            'title',
            'content',
            'city',
            'date',
            'student',
            'image_url',
            'upvotes',
            'liked',
            'bookmarked',
        ]

class CreateCommunityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityPost
        fields = [
            'title',
            'content',
            'city',
            'student',
            'image_url',
        ]

class CommentSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()


    def get_student(self,instance):
        return instance.student.name
    
    def get_liked(self,instance):
        student_id = self.context['student_id']
        student_instance = Student.objects.get(pk=student_id)
        return student_instance in instance.liked_by.all()

    class Meta:
        model = Comment
        fields = [
            'id',
            'student',
            'comment',
            'upvotes',
            'date',
            'post',
            'liked',
        ]

class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'student',
            'comment',
            'post',
        ]
        