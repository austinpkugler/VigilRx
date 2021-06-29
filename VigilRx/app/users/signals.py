from django.db.models.signals import post_save
from django.dispatch import receiver

# /home/user/Documents/reu/VigilRx/VigilRx/app
from VigilRx.bridge.patient import new_patient
from VigilRx.bridge.prescriber import new_prescriber
from VigilRx.bridge.pharmacy import new_pharmacy
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_contract(sender, instance, **kwargs):
    # Patient
    if instance.role == 1:
        new_patient(instance)
    # Prescriber
    elif instance.role == 2:
        new_prescriber(instance)
    # Pharmacy
    elif instance.role == 3:
        new_pharmacy(instance)
