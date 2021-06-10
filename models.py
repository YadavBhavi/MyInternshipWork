from django.db import models
from django.contrib.auth.models import User

types_of_orgs = models.TextChoices('types_of_orgs', 'NGO GENERAL')
types_of_roles = models.TextChoices('types_of_roles', 'WORKER ADMIN SUPERVISOR')
types_of_status = models.TextChoices('types_of_status', 'ACCEPTED PENDING REJECTED')


class Org(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    corporate_address = models.CharField(max_length=100, blank=True, default='')
    business_email = models.CharField(max_length=100, blank=True, default='')
    website = models.CharField(max_length=300, blank=True, default='')
    contact_no = models.CharField(max_length=100, blank=True, default='')
    foundation_date = models.DateField()
    location = models.CharField(max_length=300, blank=True, default='')
    # logo = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Suborg(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True, default='')
    email = models.CharField(max_length=100, blank=True, default='')
    location = models.CharField(max_length=300, blank=True, default='')
    contact_no = models.CharField(max_length=100, blank=True, default='')
    type = models.CharField(choices=types_of_orgs.choices, max_length=100)
    foundation_date = models.DateField()
    org_reference = models.ForeignKey(Org, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Invitees(models.Model):
    invitee_email = models.CharField(max_length=100, blank=True, default='')
    invitation_email_link = models.CharField(max_length=500, blank=True, default='')
    email_sent_date = models.DateField()
    org_reference = models.ForeignKey(Org, on_delete=models.CASCADE)
    suborg_reference = models.ForeignKey(Suborg, on_delete=models.CASCADE)
    role_type = models.CharField(blank=True, choices=types_of_roles.choices, max_length=100)
    status_type = models.CharField(blank=True, choices=types_of_status.choices, max_length=100)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
