from decimal import Decimal
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100)
    total_budget = models.DecimalField(
        max_digits=20, decimal_places=2, default=Decimal(0.00)
    )
    credit_score = models.DecimalField(
        max_digits=20, decimal_places=2, default=Decimal(0.00)
    )

    def __str__(self) -> str:
        return self.name


class Transaction(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="transactions"
    )
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="transactions"
    )


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class CategoryBudget(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="budget"
    )
    budget = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="budgets"
    )

    def __str__(self) -> str:
        return self.category.name + " " + self.student.name + "  " + str(self.budget)
