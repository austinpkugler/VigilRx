import os
import sys

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CustomUser

curr_dir = os.path.dirname(__file__)
bridge_dir = os.path.abspath(os.path.join(curr_dir, os.path.join('..', '..', 'bridge')))
sys.path.append(bridge_dir)


@receiver(post_save, sender=CustomUser)
def create_contract(sender, instance, created, **kwargs):
    if not instance.contract:
        # Patient
        if instance.role == 1:
            patient_contract = ''
            CustomUser.objects.filter(username=instance.username).update(contract=patient_contract)
        # Prescriber
        elif instance.role == 2:
            prescriber_contract = ''
            CustomUser.objects.filter(username=instance.username).update(contract=prescriber_contract)
        # Pharmacy
        elif instance.role == 3:
            pharmacy_contract = ''
            CustomUser.objects.filter(username=instance.username).update(contract=pharmacy_contract)
