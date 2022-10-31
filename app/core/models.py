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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country_code = models.CharField(max_length=3, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    gender = models.CharField(max_length=1, null=True)
    birthday = models.CharField(max_length=25, null=True)

    referrals = models.ManyToManyField('Referral')
    investments = models.ManyToManyField('Project')

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """Recipes object"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Company(models.Model):
    """Company"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, unique=True)
    icon = models.TextField(blank=True)
    models = models.ManyToManyField('Project')

    def __str__(self):
        return self.name


class Project(models.Model):
    """Projects"""

    company_related = models.ForeignKey(
        Company,
        on_delete=models.CASCADE
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255, unique=True)
    icon = models.TextField(blank=True)

    pre_sale_price = models.CharField(max_length=255, default='')
    pre_sale_date = models.CharField(max_length=255, default='')
    premises_delivery_date = models.CharField(max_length=255, default='')
    rent_price_approximate = models.CharField(max_length=255, default='')
    resale_price_approximate = models.CharField(max_length=255, default='')

    description = models.CharField(max_length=255)

    images = models.ManyToManyField('Image', blank=True, null=True)
    details = models.ManyToManyField('Detail')
    extras = models.ManyToManyField('Extra')

    def ___str__(self):
        return self.company


class Image(models.Model):
    """Image"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.TextField(blank=True)
    def __str__(self):
        return self.url


class Detail(models.Model):
    """Detail"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=255)
    info = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Extra(models.Model):
    """Extra"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=255)
    info = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Referral(models.Model):
    """Referral"""
    user_referral = models.ManyToManyField('User')
    project = models.ManyToManyField('Project')
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status
