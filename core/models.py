from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager,AbstractBaseUser
# Create your models here.



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    username=None
    email = models.CharField(max_length=80, unique=True)
    first_name=models.CharField(max_length=100 )
    last_name=models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20 )
    nin = models.CharField(max_length=20)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Job(models.Model):
    job_type=models.CharField(max_length=80)
    city=models.CharField(max_length=80,)
    street_adddress=models.CharField(max_length=80)
    job_description=models.CharField(max_length=80)
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="job")
    


class NewsLetterSubscriberModel(models.Model):
    email = models.CharField(max_length=80, unique=True)
    
    




    # completed=models.BooleanField()
    # dateTime=models.DateTimeField()
    