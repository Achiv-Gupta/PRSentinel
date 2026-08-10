from .models import PullRequest
from .github.client import GitHubClient


def process_pull_request(payload):
    action = payload.get("action")

    if action not in ["opened", "reopened", "synchronize", "closed"]:
        return

    pr = payload["pull_request"]

    repository = payload["repository"]["full_name"]
    pr_number = pr["number"]
    title = pr["title"]
    author = pr["user"]["login"]
    commit_sha = pr["head"]["sha"]
    status = pr["state"]

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
    files = client.get_pull_request_files(repository, pr_number)

    return files

CONFIDENCE_THRESHOLD = 0.80


def filter_issues(review_result):
    return [
        issue
        for issue in review_result.issues
        if issue.confidence >= CONFIDENCE_THRESHOLD
    ]