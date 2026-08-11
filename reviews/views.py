from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import PullRequest
from .tasks import review_pull_request


@api_view(["POST"])
def github_webhook(request):

    payload = request.data

    repository = payload["repository"]["full_name"]
    pr = payload["pull_request"]

    pr_number = pr["number"]

    PullRequest.objects.update_or_create(
        repository=repository,
        pr_number=pr_number,
        defaults={
            "title": pr["title"],
            "author": pr["user"]["login"],
            "commit_sha": pr["head"]["sha"],
            "status": pr["state"].upper(),
        },
    )

    review_pull_request.delay(
        repository,
        pr_number,
    )

    return Response({
        "message": "PR review queued"
    })