from django.contrib.auth.models import AbstractUser, UserManager, make_password
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", User.ROLES["admin"])
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["last_name", "first_name"]

    ROLES = {
        "admin": "Admin",
        "user": "User",
    }

    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=False, null=False)
    middle_name = models.CharField(_("middle name"), max_length=30, blank=True, null=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=False, null=False)
    username = None
    role = models.CharField(_("role"), max_length=5, choices=ROLES.items(), default=ROLES["user"])

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    class Meta(AbstractUser.Meta):
        ordering = ("last_name", "first_name")
        verbose_name = _("user")
        verbose_name_plural = _("users")
        swappable = "AUTH_USER_MODEL"


class InviteCode(models.Model):
    code = models.CharField(max_length=8, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invite_codes")
    role = models.CharField(max_length=5, choices=User.ROLES)
