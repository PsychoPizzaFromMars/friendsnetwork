from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Friendship(models.Model):
    STATUS_CHOICES = (
        ('pending_outgoing', 'Pending Outgoing'),
        ('pending_incoming', 'Pending Incoming'),
        ('accepted', 'Accepted'),
        ('none', 'None'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def accept(self):
        self.status = 'accepted'
        self.save()
        # Automatically create a reciprocal friendship
        Friendship.objects.get_or_create(user=self.friend, friend=self.user, status='accepted')

    def reject(self):
        self.status = 'none'
        self.save()

    def remove_friend(self):
        self.delete()
        # Delete reciprocal friendship
        Friendship.objects.filter(user=self.friend, friend=self.user).delete()