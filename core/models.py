from django.db import models
from django.contrib.auth.models import User


class Area(models.Model):
    area_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default="Ahmedabad")

    def __str__(self):
        return self.area_name


class JobType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name


class Job(models.Model):
    title = models.CharField(max_length=200)
    job_type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    duration = models.CharField(max_length=100)
    pay = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default="open")

    job_details = models.TextField(
        blank=True,
        help_text="Describe what work needs to be done"
    )

    # 🔑 OWNER FIELD (VERY IMPORTANT)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("hired", "Hired"),
        ("rejected", "Rejected"),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="applied"
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} → {self.job.title}"
    
class KYCProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    document_type = models.CharField(
        max_length=50,
        choices=[
            ("aadhaar", "Aadhaar Card"),
            ("voter", "Voter ID"),
            ("driving", "Driving License"),
        ]
    )

    document_file = models.FileField(upload_to="kyc_documents/")
    
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("verified", "Verified"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )

    submitted_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.status}"
