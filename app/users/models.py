from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    PATIENT, PRESCRIBER = 'patient', 'prescriber'
    ROLE_CHOICES = (
        (PATIENT, 'Patient'),
        (PRESCRIBER, 'Prescriber'),
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=50, null=True)
    address = models.CharField(max_length=42, null=True)
    identifier = models.CharField(max_length=9, null=True)

    def __str__(self):
        return f'{self.user.username}'
