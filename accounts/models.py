from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class ExpenseManagerUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    first_name=models.CharField(blank=False,null=False,max_length=30)
    last_name=models.CharField(blank=False,null=False,max_length=30)
    date_registered=models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)


    objects=UserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table='expensemanager_user'
        verbose_name='expensemanager_user'
        verbose_name_plural='expensemanager_users'

class Expenditure(models.Model):
    title=models.CharField(max_length=100,blank=False)
    category=models.CharField(max_length=100,blank=False)
    recipient_phone=models.CharField(max_length=13,blank=False)
    recipient_name=models.CharField(max_length=50,blank=False)
    donor=models.ForeignKey(ExpenseManagerUser,on_delete=models.CASCADE)
    date_registered=models.DateTimeField(auto_now_add=True)
    event_date=models.DateField()
    amount_spent=models.DecimalField(decimal_places=2,max_digits=10)
    payement_method=models.CharField(max_length=40,blank=False)


    class Meta:
        db_table='expenditure'
class Revenue(models.Model):
    service_offered=models.CharField(max_length=32,blank=False)
    payer_contact=models.CharField(max_length=13,blank=False)
    payer_name=models.CharField(max_length=50,blank=False)
    receiver=models.ForeignKey(ExpenseManagerUser,on_delete=models.CASCADE)
    payment_method=models.CharField(max_length=20,blank=False)
    date_recorded=models.DateTimeField(auto_now_add=True)
    amount_received=models.DecimalField(decimal_places=2,max_digits=10)

    class Meta:
        db_table='revenue'
