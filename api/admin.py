from django.contrib import admin
from .models import Student, Category, CategoryBudget, Transaction

# Register your models here.


class StudentView(admin.ModelAdmin):
    readonly_fields = (
        "id",
        "budgets",
    )

    def budgets(self, instance):
        return [f"{m}" for m in instance.budgets.all()]


admin.site.register(Student, StudentView)
admin.site.register(Category)
admin.site.register(CategoryBudget)
admin.site.register(Transaction)
