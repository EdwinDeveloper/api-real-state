"""
    Database models
"""
import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user"""
        if not email:
            raise ValueError("User mush have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    country_code = models.CharField(max_length=3)
    phone_number = models.CharField(max_length=12)
    gender = models.CharField(max_length=1)
    birthday = models.CharField(max_length=25)
    # referrals = models.ManyToManyField('Referral')
    # investments = models.ManyToManyField('Project')
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """Recipes object"""
    user = models.ForeignKey(  # Many recipes can bellow to a simple user
        settings.AUTH_USER_MODEL,  # Reference of the user
        on_delete=models.CASCADE,
        # CASCADE : If we delete a user, all the recipes /
        # asociated to this user will be gone
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # Contain more content
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Project(models.Model):
    """Projects"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    prices = models.ManyToManyField('Price')
    description = models.CharField(max_length=255)
    details = models.ManyToManyField('Detail')
    aditionalInfos = models.ManyToManyField('AditionalInfo')

    def ___str__(self):
        return self.company


class Price(models.Model):
    """Prices"""

    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Detail(models.Model):
    """Detail"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# class Image(models.Model):
#     """Image"""
#     name = models.CharField(max_length=255)
#     url = models.ImageField(blank=True)


class AditionalInfo(models.Model):
    """Aditional Info"""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# class Referral(models.Model):
#     """Referral"""
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#     )
#     status = models.CharField(max_length=10)
#     project = models.ForeignKey(
#         Project,
#         on_delete=models.CASCADE,
#     )

#     def __str__(self):
#         return self.status
