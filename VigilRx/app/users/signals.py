import os
import sys

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser

curr_dir = os.path.dirname(__file__)
bridge_dir = os.path.abspath(os.path.join(curr_dir, os.path.join('..', '..', 'bridge')))
sys.path.append(bridge_dir)

from registrar import new_patient, new_prescriber, new_pharmacy


@receiver(post_save, sender=CustomUser)
def create_contract(sender, instance, created, **kwargs):
    if not instance.contract:
        # Patient
        if instance.role == 1:
            patient_contract = new_patient(instance)
            CustomUser.objects.filter(username=instance.username).update(contract=patient_contract)
        # Prescriber
        elif instance.role == 2:
            contract = new_prescriber(instance)
        # Pharmacy
        elif instance.role == 3:
            contract = new_pharmacy(instance)

