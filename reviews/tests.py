import hashlib
import hmac
import json

from django.conf import settings
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from unittest.mock import patch
from reviews.llm.parser import parse_llm_response
from reviews.models import Review

@override_settings(GITHUB_WEBHOOK_SECRET="test-secret")
class WebhookTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = "/github/webhook/"

        self.payload = {
            "repository": {
                "full_name": "test/repo",
            },
            "pull_request": {
                "number": 1,
                "title": "Test PR",
                "state": "open",
                "user": {
                    "login": "tester",
                },
                "head": {
                    "sha": "abc123",
                },
            },
            "action": "opened",
        }

    def _signature(self, body):
        digest = hmac.new(
            b"test-secret",
            body,
            hashlib.sha256,
        ).hexdigest()

        return f"sha256={digest}"

    @patch("reviews.views.review_pull_request.delay")
    def test_valid_signature(self, mock_delay):
        body = json.dumps(self.payload).encode()

        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_X_GITHUB_EVENT="pull_request",
            HTTP_X_HUB_SIGNATURE_256=self._signature(body),
        )

        self.assertEqual(response.status_code, 200)
        mock_delay.assert_called_once_with("test/repo", 1)

    def test_invalid_signature(self):
        body = json.dumps(self.payload).encode()

        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_X_GITHUB_EVENT="pull_request",
            HTTP_X_HUB_SIGNATURE_256="sha256=invalid",
        )

        self.assertEqual(response.status_code, 401)

    def test_missing_signature(self):
        body = json.dumps(self.payload).encode()

        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_X_GITHUB_EVENT="pull_request",
        )

        self.assertEqual(response.status_code, 401)

    @patch("reviews.views.review_pull_request.delay")
    def test_non_pull_request_event_is_ignored(self, mock_delay):
        body = json.dumps(self.payload).encode()

        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_X_GITHUB_EVENT="push",
            HTTP_X_HUB_SIGNATURE_256=self._signature(body),
        )

        self.assertEqual(response.status_code, 200)
        mock_delay.assert_not_called()


    @patch("reviews.views.review_pull_request.delay")
    def test_irrelevant_pull_request_action_is_ignored(self, mock_delay):
        payload = self.payload.copy()
        payload["action"] = "closed"

        body = json.dumps(payload).encode()

        response = self.client.post(
            self.url,
            data=body,
            content_type="application/json",
            HTTP_X_GITHUB_EVENT="pull_request",
            HTTP_X_HUB_SIGNATURE_256=self._signature(body),
        )

        self.assertEqual(response.status_code, 200)
        mock_delay.assert_not_called()



class LLMParserTests(TestCase):

    def valid_issue(self):
        return {
            "issue_type": "bug",
            "severity": "high",
            "confidence": 0.95,
            "file": "calculator.py",
            "line_content": "return a - b",
            "description": "Addition function performs subtraction.",
            "suggestion": "Use a + b instead.",
        }

    def test_valid_json(self):
        payload = {
            "issues": [self.valid_issue()]
        }

        result = parse_llm_response(json.dumps(payload))

        self.assertEqual(len(result.issues), 1)
        self.assertEqual(result.issues[0].issue_type, "bug")

    def test_markdown_json(self):
        payload = {
            "issues": [self.valid_issue()]
        }

        raw = f"```json\n{json.dumps(payload)}\n```"

        result = parse_llm_response(raw)

        self.assertEqual(len(result.issues), 1)

    def test_invalid_json(self):
        with self.assertRaises(ValueError):
            parse_llm_response("{invalid json}")

    def test_invalid_schema(self):
        payload = {
            "issues": [
                {
                    **self.valid_issue(),
                    "severity": "super_high",
                }
            ]
        }

        with self.assertRaises(ValueError):
            parse_llm_response(json.dumps(payload))


class IdempotencyTests(TestCase):

    def test_same_commit_is_not_reviewed_twice(self):
        first, created_first = Review.objects.get_or_create(
            repository="test/repo",
            pr_number=1,
            commit_sha="abc123",
        )

        second, created_second = Review.objects.get_or_create(
            repository="test/repo",
            pr_number=1,
            commit_sha="abc123",
        )

        self.assertTrue(created_first)
        self.assertFalse(created_second)

        self.assertEqual(
            Review.objects.filter(
                repository="test/repo",
                pr_number=1,
                commit_sha="abc123",
            ).count(),
            1,
        )
    
    def test_new_commit_creates_new_review(self):
        Review.objects.create(
            repository="test/repo",
            pr_number=1,
            commit_sha="abc123",
        )

        _, created = Review.objects.get_or_create(
            repository="test/repo",
            pr_number=1,
            commit_sha="def456",
        )

        self.assertTrue(created)