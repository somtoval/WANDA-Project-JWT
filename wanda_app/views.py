from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .models import Author, Submission, SubmissionStatus
from .serializers import RegisterSerializer, SubmissionSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from .permissions import IsAdminGroup  # Import the custom permission

from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPagination

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
            print("THe USER IS : ", user)
            group = Group.objects.get(name='author')  # Ensure the group exists
            user.groups.add(group)
            return Response({"message": "User and Author registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login endpoint
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"message": "Logged in successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# Logout endpoint
@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

class SubmissionView(ListCreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Define filterable fields
    filterset_fields = ['approved', 'author__user__username']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    
    # Restrict creation to authenticated users
    permission_classes = [IsAuthenticated]

    # Use the custom pagination class
    pagination_class = CustomPagination  

    def perform_create(self, serializer):
        """
            Automatically set the author as the logged-in user
            Note this works because I am using the "author_profile" related name
            The related_name attribute in Django models is used to specify the reverse relation from the related model back to the model that defines the relationship. It helps in accessing the related objects in a more readable way.
        """
        serializer.save(author=self.request.user.author_profile)

class ApprovalView(APIView):
    permission_classes = [IsAdminGroup]  # Apply the custom permission

    def post(self, request, submission_id):
        """
        Approve a submission by its ID by setting its status to APPROVED.
        """
        try:
            # Fetch the submission by its ID
            submission = Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            return Response({"error": "Submission not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update the submission's status to APPROVED
        submission.status = SubmissionStatus.APPROVED
        submission.save()

        return Response({"message": "Submission approved successfully"}, status=status.HTTP_200_OK)
    
class DisapprovalView(APIView):
    permission_classes = [IsAdminGroup]  # Apply the custom permission

    def post(self, request, submission_id):
        """
        Disapprove a submission by its ID.
        """
        try:
            # Fetch the submission by its ID
            submission = Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            return Response({"error": "Submission not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update the submission's status to DISAPPROVED
        submission.status = SubmissionStatus.DISAPPROVED
        submission.save()

        return Response({"message": "Submission disapproved successfully"}, status=status.HTTP_200_OK)