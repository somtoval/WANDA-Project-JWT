from django.contrib.auth.models import User
from django.db import models
import uuid

# Define the Author model
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_profile')

    def __str__(self):
        return self.user.username

# # Define the Submission model
# class Submission(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='submissions')
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     approved = models.BooleanField(default=False)
#     file = models.FileField(upload_to='submissions/')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title

# Define the choices for submission status
class SubmissionStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    DISAPPROVED = 'disapproved', 'Disapproved'

class Submission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='submissions')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=11,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.PENDING,
    )
    file = models.FileField(upload_to='submissions/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title