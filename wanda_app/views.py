from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .models import Author, Submission, SubmissionStatus
from .serializers import RegisterSerializer, SubmissionSerializer
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from .permissions import IsAdminGroup
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny

from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPagination
from rest_framework_simplejwt.tokens import RefreshToken
from .filters import SubmissionFilter

# CSRF token endpoint
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    Endpoint to get CSRF token - will set CSRF cookie if it's not already set
    """
    return JsonResponse({'csrfToken': get_token(request)})

# Register endpoint
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Save the Author instance
            author = serializer.save()
            # Access the related User object
            user = author.user
            group = Group.objects.get(name='author')
            user.groups.add(group)
            
            # Log the user in after registration
            login(request, user)
            
            return Response({
                "message": "User and Author registered successfully",
                "username": user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login endpoint
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                "error": "Both username and password are required"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        user = authenticate(request, username=username, password=password)
        
        # if user is not None:
        #     login(request, user)
        #     return Response({
        #         "message": "Logged in successfully",
        #         "username": user.username,
        #         "isAuthenticated": True
        #     }, status=status.HTTP_200_OK)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({
            "error": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)

    @method_decorator(csrf_exempt)
    def get(self, request):
        """
        Check authentication status
        """
        if request.user.is_authenticated:
            return Response({
                "isAuthenticated": True,
                "username": request.user.username
            })
        return Response({
            "isAuthenticated": False
        })

class LogoutView(APIView):
    permission_classes = [AllowAny]  # Explicitly allow unauthenticated access

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

class SubmissionView(ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SubmissionFilter  # Use the custom filter class
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author_profile)

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ApprovalView(APIView):
    permission_classes = [IsAdminGroup]

    @method_decorator(csrf_exempt)
    def post(self, request, submission_id):
        try:
            submission = Submission.objects.get(id=submission_id)
            submission.status = SubmissionStatus.APPROVED
            submission.save()
            return Response({
                "message": "Submission approved successfully"
            }, status=status.HTTP_200_OK)
        except Submission.DoesNotExist:
            return Response({
                "error": "Submission not found"
            }, status=status.HTTP_404_NOT_FOUND)

class DisapprovalView(APIView):
    permission_classes = [IsAdminGroup]

    @method_decorator(csrf_exempt)
    def post(self, request, submission_id):
        try:
            submission = Submission.objects.get(id=submission_id)
            submission.status = SubmissionStatus.DISAPPROVED
            submission.save()
            return Response({
                "message": "Submission disapproved successfully"
            }, status=status.HTTP_200_OK)
        except Submission.DoesNotExist:
            return Response({
                "error": "Submission not found"
            }, status=status.HTTP_404_NOT_FOUND)
        
# CSRF token endpoint
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    Endpoint to get CSRF token - will set CSRF cookie if it's not already set
    """
    return JsonResponse({'csrfToken': get_token(request)})