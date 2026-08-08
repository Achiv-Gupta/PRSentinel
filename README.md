# PRSentinel
AI-Powered PR Review Agent

As AI-assisted coding accelerates how fast code gets written, code review has become the real bottleneck — not code generation. This project addresses that directly: a Django backend that listens for GitHub pull request events via webhooks, runs the diff through an LLM to flag bugs, security issues, missing test coverage, and style violations, and posts high-confidence findings back as inline PR comments — automatically, within seconds of a PR being opened or updated.

Built with Django, Celery, Redis, Postgres, and the GitHub REST API, fully containerized with Docker Compose.
