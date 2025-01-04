from django.urls import path
from .views import RegisterView, LoginView, LogoutView, SubmissionView,ApprovalView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('submissions/', SubmissionView.as_view(), name='submission-list-create'),
    path('submissions/<uuid:submission_id>/approve/', ApprovalView.as_view(), name='submission-approve'),
]
