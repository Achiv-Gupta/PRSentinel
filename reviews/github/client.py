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

        url = f"{self.BASE_URL}/repos/{repo}/pulls/{number}"

        response = requests.get(
            url,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()
    
    def get_pull_request_files(self, repo, number):

        url = f"{self.BASE_URL}/repos/{repo}/pulls/{number}/files"

        response = requests.get(
            url,
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()
    
    def create_review_comment(
        self,
        repo,
        pr_number,
        body,
        commit_id,
        path,
        line,
    ):
        url = (
            f"{self.BASE_URL}/repos/"
            f"{repo}/pulls/{pr_number}/comments"
        )

        payload = {
            "body": body,
            "commit_id": commit_id,
            "path": path,
            "line": line,
            "side": "RIGHT",
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
        )

        response.raise_for_status()

        return response.json()
