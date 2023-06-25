from decimal import Decimal
from django.db import models
from django.core.validators import MinLengthValidator


class Student(models.Model):
    name = models.CharField(max_length=100,blank=False)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100,blank=False)
    total_budget = models.DecimalField(
        max_digits=20, decimal_places=2,default=Decimal(0.00)
    )
    credit_score = models.DecimalField(
        max_digits=20, decimal_places=2, default=Decimal(10.00)
    )

    def __str__(self) -> str:
        return self.name


class Transaction(models.Model):
    title = models.CharField(max_length=100,blank=False)
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="transactions"
    )
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="transactions"
    )

    class Meta:
        ordering = ['-date','-id']

    def __str__(self) -> str:
        return self.title + " " + str(self.student)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class CategoryBudget(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="budget"
    )
    budget = models.DecimalField(max_digits=20, decimal_places=2)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="budgets"
    )

    def __str__(self) -> str:
        return self.category.name + " " + self.student.name + "  " + str(self.budget)
    

class CommunityPost(models.Model):
    title = models.CharField(max_length=50,blank=False)
    content = models.TextField(blank=False,editable=True,validators=[MinLengthValidator(20)])
    student = models.ForeignKey(Student,related_name='posts',on_delete=models.CASCADE)
    city = models.CharField(max_length=30,blank=False)
    liked_by = models.ManyToManyField(Student,related_name='liked_posts',blank=True)
    bookmarked_by = models.ManyToManyField(Student,related_name='bookmarked_posts',blank=True)
    upvotes = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    image_url = models.URLField(blank=True,null=True)

    class Meta:
        ordering = ['-upvotes']


class Comment(models.Model):
    comment = models.TextField(blank=False,editable=True,validators=[MinLengthValidator(20)])
    student = models.ForeignKey(Student,related_name='comments',on_delete=models.CASCADE)
    post = models.ForeignKey(CommunityPost,related_name='comments',on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(Student,related_name='liked_comments',blank=True)
    upvotes = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['-upvotes']

