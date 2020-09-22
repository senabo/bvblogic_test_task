from django.db import models
from django.contrib.auth import get_user_model

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


User = get_user_model()


class UserProfile(models.Model):
    """User's profile with additional information"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=60, default="")
    about = models.TextField(max_length=1500, default="", blank=True)
    avatar = models.ImageField(null=True, blank=True)
    is_moderator = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def set_user_as_moderator(self):
        self.is_moderator = True
        self.save()


# Send email for password reset
@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):

    email_plaintext_message = "{}?token={}".format(
        reverse("password_reset:reset-password-request"), reset_password_token.key
    )

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email],
    )
