from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from django.urls import reverse
from django.utils import timezone

from django.db import models


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, display_name=None, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not display_name:
            display_name = username

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            display_name=display_name
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,  username, display_name, password):
        user = self.create_user( email, username,display_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    display_name = models.CharField(max_length=140)
    bio = models.CharField(max_length=140, blank=True, default="")
    avatar = models.ImageField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["display_name", "username"]

    def __str__(self):
        return "@{}".format(self.username)

    def get_short_name(self):
        return self.display_name

    def get_long_name(self):
        return "{} @{}".format(self.username)

    def get_absolute_url(self):
        return reverse('accounts:profile-update', kwargs={'pk': self.pk})

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Skill(models.Model):
    user = models.ForeignKey(User, related_name='skill',
                             on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=255, unique=True)


class Project(models.Model):
    owner = models.ForeignKey(User, related_name='project',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=140)
    timeline = models.CharField(max_length=100)
    app_requirements = models.CharField(max_length=100)


class Position(models.Model):
    project = models.ForeignKey(Project, related_name='project',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=40, unique=True)
    description = models.CharField(max_length=140)


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('accounts:profile-update', kwargs={'pk': self.pk})

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)


class FamilyMember(models.Model):
    profile = models.ForeignKey(Profile, related_name='familymember',
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)

