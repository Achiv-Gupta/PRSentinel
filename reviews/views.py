from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import PullRequest
from .tasks import review_pull_request

import hashlib
import hmac

from django.conf import settings


@api_view(["POST"])
def github_webhook(request):

    signature = request.headers.get("X-Hub-Signature-256")

    if not signature:
        return Response(
            {"error": "Missing webhook signature"},
            status=401,
        )

    expected_signature = (
        "sha256="
        + hmac.new(
            settings.GITHUB_WEBHOOK_SECRET.encode(),
            request.body,
            hashlib.sha256,
        ).hexdigest()
    )

    if not hmac.compare_digest(
        signature,
        expected_signature,
    ):
        return Response(
            {"error": "Invalid webhook signature"},
            status=401,
        )

    # Signature verified — process webhook
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