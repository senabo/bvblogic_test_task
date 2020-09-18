from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

COMMENT_STATUS_OPTIONS = (
    ("created", "Comment created"),
    ("updated", "Comment was updated"),
    ("deleted", "Comment was deleted"),
)


class Topic(models.Model):
    """Model for user's topic on forum"""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="topic_author"
    )
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    closed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Model for comments in topics"""

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_author"
    )
    content = models.CharField(max_length=250)

    # Comment has 3 statuses: created, updated or deleted. Default is created
    status = models.CharField(
        max_length=60, choices=COMMENT_STATUS_OPTIONS, default="created"
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    def update_comment(self):
        self.status = "updated"
        self.save()

    def delete_comment(self):
        """Don't delete comment from bd. Only change content and status"""
        self.content = "Comment was deleted"
        self.status = "deleted"
        self.save()
