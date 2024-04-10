# import os
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

# from django.contrib.gis.db import models


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    LANGUAGE_CHOICES = [
        # ("en", "English"),
        ("pt-br", "Portugues"),
    ]
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    preferred_language = models.CharField(
        max_length=5, choices=LANGUAGE_CHOICES, default="pt-br"
    )
    query_balance = models.IntegerField(default=100)
    doc_balance = models.IntegerField(default=50)
    query_credits = models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Topic(models.Model):
    """Topic model"""

    TOPIC_TYPES = [
        ("ge", "Geral"),
        ("es", "Estudos"),
        ("jr", "Jurídico"),
        ("sa", "Medicina e Saúde"),
        ("ci", "Ciência"),
        ("tc", "Tecnologia"),
        ("an", "Cuidado de Animais"),
        ("nr", "Normas"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)
    type = models.CharField(max_length=2, choices=TOPIC_TYPES, default="ge")

    def type_name(self):
        return self.get_type_display()


class TopicInvite(models.Model):
    """Topic invite model"""

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class TopicInviteSent(models.Model):
    """Topic send invite model"""

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def accepted(self):
        if TopicInvite.objects.filter(
            topic=self.topic, user__email=self.email
        ).exists():
            return True
        return False


class Document(models.Model):
    """Document model"""

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    base_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, default="OK")

    class Meta:
        ordering = ["-id"]


class DocumentBody(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    doc = models.BinaryField()
    type = models.CharField(max_length=100)


class Question(models.Model):
    """Question model"""

    text = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    answer = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    cost = models.FloatField(null=True, blank=True)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-id"]
