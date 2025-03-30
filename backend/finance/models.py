from django.db import models
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.db.models import F

# Create your models here.
class FinUser(models.Model):
    name = models.CharField(max_length=100)
    income = models.DecimalField(null=True, blank=True, default=0, max_digits=10, decimal_places=2) # income for main user, for this user is expence
    expence = models.DecimalField(null=True, blank=True, default=0, max_digits=10, decimal_places=2) # expence for main user, for this user is income
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Transactions(models.Model):
    fin_user = models.ForeignKey(FinUser, on_delete=models.PROTECT)
    disc = models.CharField(max_length=500, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_income = models.BooleanField(default=True) # income for main user, for this user is expence
    created_on = models.DateField(auto_now_add=True)


@receiver(post_save, sender=Transactions)
def add_in_fin_user(sender, instance, created, **kwargs):
    if instance.amount:
        if instance.is_income:
            FinUser.objects.filter(id=instance.fin_user.id).update(income=F('income')+instance.amount)
        else:
            FinUser.objects.filter(id=instance.fin_user.id).update(expence=F('expence')+instance.amount)

@receiver(post_delete, sender=Transactions)
def delete_in_fin_user(sender, instance, **kwargs):
    if instance.amount:
        if instance.is_income:
            FinUser.objects.filter(id=instance.fin_user.id).update(income=F('income')-instance.amount)
        else:
            FinUser.objects.filter(id=instance.fin_user.id).update(expence=F('expence')-instance.amount)

class ITCompany(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.IntegerField(null=True,blank=True)
    email = models.EmailField(null=True, blank=True)
    apply_on = models.DateTimeField(null=True, blank=True)
    interview_on = models.DateTimeField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    job_role = models.CharField(max_length=100, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    more = models.TextField(null=True,blank=True)