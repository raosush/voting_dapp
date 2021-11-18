from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, username
        and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, username
        and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    # Fields
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    confirmation_token = models.CharField(max_length=64, null=True)
    confirmation_token_sat = models.DateTimeField(verbose_name='confirmation_token_sent_at_time_stamp', null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def to_payload(self):
        return { 'id': self.id, 'username': self.username, 'email': self.email }

class Profile(models.Model):
    name = models.CharField(verbose_name='name_of_the_user', max_length=128)
    about_me = models.TextField(verbose_name='explain_about_yourself', max_length=65535)
    experience = models.TextField(verbose_name='any_relevant_experience', max_length=65535)
    social_profile = models.URLField(verbose_name='link_to_any_social_profile', null=True, blank=True, max_length=255)
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user) + "'s Profile" + " - " + str(self.pk)
