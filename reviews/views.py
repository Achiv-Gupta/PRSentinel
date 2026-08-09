from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import PullRequest
from .github.client import GitHubClient

@api_view(["POST"])
def github_webhook(request):

    payload = request.data

    #.get because it can be none and still there will be no error
    action = payload.get("action")

    if action not in ["opened", "reopened", "synchronize", "closed"]:
        return Response({"message": "Ignored"})

    pr = payload["pull_request"]

    repository = payload["repository"]["full_name"]
    pr_number = pr["number"]
    title = pr["title"]
    author = pr["user"]["login"]
    commit_sha = pr["head"]["sha"]
    status = pr["state"]

    # print(repository)
    # print(pr_number)
    # print(title)
    # print(author)
    # print(commit_sha)
    # print(status)

    PullRequest.objects.update_or_create(
    repository=repository,
    pr_number=pr_number,
    defaults={
        "title": title,
        "author": author,
        "commit_sha": commit_sha,
        "status": status.upper(),
    },
    )
    client = GitHubClient()

    files = client.get_pull_request(
        repository,
        pr_number
    )

    for file in files:

        print("=" * 50)

        print(file["filename"])

        print(file["status"])

        print(file["patch"])

        print("=" * 50)

    return Response({"message": "Saved"})


