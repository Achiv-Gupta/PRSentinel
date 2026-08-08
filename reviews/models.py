from django.db import models

class PullRequest(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("CLOSED", "Closed"),
        ("MERGED", "Merged"),
    ]

    repository = models.CharField(max_length=255)
    pr_number = models.IntegerField()
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=255)
    commit_sha = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PR #{self.pr_number} - {self.title}"