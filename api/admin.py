from django.contrib import admin
from .models import Student, Category, CategoryBudget, Transaction, CommunityPost, Comment

# Register your models here.


class StudentView(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "budgets",
    )

    def budgets(self, instance):
        return [f"{m}" for m in instance.budgets.all()]
    
class CategoryView(admin.ModelAdmin):
    readonly_fields = (
        "id",
    )


admin.site.register(Student, StudentView)
admin.site.register(Category,CategoryView)
admin.site.register(CategoryBudget)
admin.site.register(Transaction)
admin.site.register(CommunityPost)
admin.site.register(Comment)
