import requests

from celery import shared_task

from .services import process_pull_request


@shared_task(
    bind=True,
    autoretry_for=(
        ValueError,
        requests.exceptions.RequestException,
    ),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def review_pull_request(self, repo, pr_number):
    process_pull_request(repo, pr_number)