from django.urls import path
from api import views

urlpatterns = [
    path('student/create/',views.StudentCreateView.as_view()),
    path('student/retrieve/<email>',views.StudentRetrieveView.as_view()),
    path('student/update/<pk>',views.StudentUpdateView.as_view()),
    path('student/monthlyExpenses/<student_id>',views.monthlyExpenses),
    path('transaction/create/',views.TransactionCreateView.as_view()),
    path('transaction/delete/<pk>',views.TransactionDeleteView.as_view()),
    path('transaction/update/<pk>',views.TransactionUpdateView.as_view()),
    path('communityPost/create/',views.CommunityPostCreateView.as_view()),
    path('communityPost/list/<int:student_id>',views.CommunityPostListView.as_view()),
    path('communityPost/update/like/<pk>',views.LikeCommunityPostView.as_view()),
    path('communityPost/update/bookmark/<pk>',views.BookmarkCommunityPostView.as_view()),
    path('comment/create/',views.CommentCreateView.as_view()),
    path('comment/list/<int:student_id>',views.CommentListView.as_view()),
    path('addCategoryBudget/',views.addCategoryBudget),
]