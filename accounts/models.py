from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ("job_poster", "Job Poster"),
        ("job_seeker", "Job Seeker"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    @property
    def is_poster(self):
        return self.role == "job_poster"

    @property
    def is_seeker(self):
        return self.role == "job_seeker"
