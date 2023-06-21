from rest_framework import serializers
from .models import Student,Transaction
import json
from django.forms.models import model_to_dict

class StudentSerializer(serializers.ModelSerializer):
    budgets = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()

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
                "title": transaction.title,
                "date": transaction.date,
                "amount": transaction.amount,
                "category": transaction.category.name
            }
            result.append(m)
        return result
    

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
        ]