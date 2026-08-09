import os 
import requests


class GitHubClient:

    BASE_URL = 'https://api.github.com'

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
            "Accept": "application/vnd.github+json"
        }

    def get_pull_request(self, repo, number):

        url = f"{self.BASE_URL}/repos/{repo}/pulls/{number}/files"

        response = requests.get(
            url,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()