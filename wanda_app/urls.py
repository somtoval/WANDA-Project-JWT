from django.urls import path
from .views import RegisterView, LoginView, LogoutView, SubmissionView,ApprovalView,DisapprovalView,get_csrf_token

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('submissions/', SubmissionView.as_view(), name='submission-list-create'),
    path('submissions/<uuid:submission_id>/approve/', ApprovalView.as_view(), name='submission-approve'),
    path('submissions/<uuid:submission_id>/disapprove/', DisapprovalView.as_view(), name='submission-disapprove'),
    
    path('get-csrf-token/', get_csrf_token, name='get-csrf-token'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
