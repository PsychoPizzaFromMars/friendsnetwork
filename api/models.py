from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    friends = models.ManyToManyField("User", blank=True)


class Friendship(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="outgoing_request"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="incoming_request"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["from_user", "to_user"], name="unique_friend_request"
            ),
            models.CheckConstraint(
                check=~models.Q(from_user=models.F("to_user")),
                name="self_request_check",
            ),
        ]
