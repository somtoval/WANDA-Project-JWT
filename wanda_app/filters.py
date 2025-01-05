import django_filters
from .models import Submission, SubmissionStatus

class SubmissionFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        field_name="status", 
        choices=[
            (SubmissionStatus.PENDING, 'Pending'),
            (SubmissionStatus.APPROVED, 'Approved'),
            (SubmissionStatus.DISAPPROVED, 'Disapproved'),
        ]
    )

    class Meta:
        model = Submission
        fields = ['status', 'author__user__username']
