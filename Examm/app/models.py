from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin,
    AbstractBaseUser,
    AbstractUser
)
from app.managers import CustomUserManager

from django.utils.text import slugify


# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images')
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Events"
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) + '-' + slugify(self.price)

        super(Event, self).save(*args, **kwargs)


class Member(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Members"
        ordering = ('-created_at',)

    def __str__(self):
        return self.full_name


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []


# class Founders(models.Model):
#     founder_name = models.CharField(max_length=100)
#     co_founder_name = models.CharField(max_length=100)
#     title = models.CharField(max_length=50)
#     body = models.TextField()
#     founder_image = models.ImageField(upload_to='images')
#     co_founder_image = models.ImageField(upload_to='images')
#
#     class Meta:
#         verbose_name_plural = "Founders"
#
#     def __str__(self):
#         return self.title
#
#
# class Order(models.Model):
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)


class People(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def str(self):
        return self.email


class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def str(self):
        return self.full_name
