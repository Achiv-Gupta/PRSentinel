from django.contrib import admin

from .models import PullRequest, Review


@admin.register(PullRequest)
class PullRequestAdmin(admin.ModelAdmin):
    list_display = (
        "repository",
        "pr_number",
        "title",
        "author",
        "status",
        "created_at",
    )

    list_filter = ("status",)

    search_fields = (
        "repository",
        "title",
        "author",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "repository",
        "pr_number",
        "commit_sha",
        "status",
        "created_at",
    )

    list_filter = ("status",)

    search_fields = (
        "repository",
        "commit_sha",
    )