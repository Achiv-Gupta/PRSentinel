# PRSentinel

## AI-Powered Pull Request Review Agent

As AI-assisted coding accelerates how fast code gets written, code review has become the real bottleneck — not code generation.

**PRSentinel** is an AI-powered backend system that automates Pull Request code reviews. It listens for GitHub Pull Request events through webhooks, analyzes the code changes using an LLM, identifies potential bugs, security issues, missing test coverage, and style violations, and posts high-confidence findings back to the Pull Request as inline comments.

The goal is simple: **give developers useful code-review feedback automatically, without waiting for a manual review.**

---

## ✨ Features

* 🔗 **GitHub Webhook Integration** — Automatically reacts to Pull Request events.
* 🤖 **AI-Powered Code Analysis** — Uses an LLM to analyze Pull Request changes.
* 🐛 **Bug Detection** — Identifies potential issues in submitted code.
* 🔐 **Security Analysis** — Flags potential security-related problems.
* 🧪 **Test Coverage Checks** — Identifies areas where additional tests may be required.
* 🎨 **Code Quality & Style Review** — Detects potential style and quality violations.
* 💬 **Inline PR Comments** — Posts high-confidence findings directly back to GitHub.
* ⚡ **Asynchronous Processing** — Uses Celery and Redis to process reviews in the background.
* 🐘 **Persistent Storage** — Uses PostgreSQL for storing application data and review information.
* 🐳 **Containerized Environment** — Built with Docker and Docker Compose.

---

## 🏗️ Architecture

```text
                         ┌─────────────────┐
                         │   GitHub PR     │
                         └────────┬────────┘
                                  │
                                  │ Webhook
                                  ▼
                         ┌─────────────────┐
                         │   Django API    │
                         └────────┬────────┘
                                  │
                                  │ Queue Task
                                  ▼
                         ┌─────────────────┐
                         │ Celery + Redis  │
                         └────────┬────────┘
                                  │
                                  │ Process PR
                                  ▼
                         ┌─────────────────┐
                         │   LLM Analysis  │
                         └────────┬────────┘
                                  │
                                  │ Findings
                                  ▼
                         ┌─────────────────┐
                         │ GitHub REST API │
                         └────────┬────────┘
                                  │
                                  │ Inline Comments
                                  ▼
                         ┌─────────────────┐
                         │   GitHub PR     │
                         └─────────────────┘

                                  │
                                  ▼
                         ┌─────────────────┐
                         │   PostgreSQL    │
                         └─────────────────┘
```

---

## 🔄 How It Works

1. A developer opens or updates a Pull Request on GitHub.
2. GitHub sends the Pull Request event to PRSentinel through a webhook.
3. The Django backend receives the event.
4. The review task is processed asynchronously using Celery and Redis.
5. The Pull Request changes are analyzed using an LLM.
6. PRSentinel identifies potential bugs, security issues, missing tests, and style violations.
7. High-confidence findings are sent back to GitHub.
8. Findings appear as inline comments on the Pull Request.
9. Review information is persisted using PostgreSQL.

---

## 🛠️ Tech Stack

| Component                | Technology             |
| ------------------------ | ---------------------- |
| Backend                  | Python, Django         |
| API                      | Django REST Framework  |
| Database                 | PostgreSQL             |
| Background Processing    | Celery                 |
| Message Broker           | Redis                  |
| AI / LLM                 | OpenAI API             |
| Code Hosting Integration | GitHub REST API        |
| Event Integration        | GitHub Webhooks        |
| Containerization         | Docker, Docker Compose |

---

## 📁 Project Structure

```text
PRSentinel/
│
├── reviews/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── tasks.py
│   └── ...
│
├── config/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

> The structure above highlights the main application components. Refer to the repository for the complete implementation.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

* Python
* Docker
* Docker Compose
* Git

### Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd PRSentinel
```

### Environment Variables

Create a `.env` file and configure the required application credentials and settings.

```env
OPENAI_API_KEY=your_api_key
GITHUB_TOKEN=your_github_token
```

Add any other environment variables required by your local configuration.

### Run with Docker Compose

```bash
docker compose up --build
```

This starts the application together with its supporting services.

---

## 🔌 GitHub Integration

PRSentinel uses **GitHub Webhooks** to react to Pull Request activity.

When a relevant Pull Request event occurs:

```text
GitHub
   │
   │ Webhook
   ▼
PRSentinel
   │
   │ Background Task
   ▼
Celery Worker
   │
   │ LLM Analysis
   ▼
Review Findings
   │
   ▼
GitHub Inline Comments
```

This allows code review to happen automatically whenever a Pull Request is opened or updated.

---

## ⚡ Background Processing

LLM-based code review can involve external API calls and processing time.

PRSentinel therefore uses:

* **Celery** for asynchronous task execution
* **Redis** as the message broker

Instead of keeping the webhook request waiting for the complete review, the review work can be handled by a background worker.

This creates a cleaner separation between:

```text
Webhook Handling
       ↓
Task Queue
       ↓
Background Processing
       ↓
AI Review
       ↓
GitHub Response
```

---

## 🤖 AI Code Review

PRSentinel sends Pull Request changes through an LLM-based review pipeline.

The review focuses on areas such as:

### Bugs

Potential logical or implementation issues that could cause unexpected behavior.

### Security

Potential security vulnerabilities or unsafe coding patterns.

### Testing

Areas where additional test coverage may be useful.

### Code Quality

Potential style, maintainability, and quality issues.

Only high-confidence findings are intended to be surfaced as Pull Request comments to reduce unnecessary review noise.

---

## 🐳 Docker

PRSentinel uses Docker and Docker Compose to simplify the development environment and run the backend together with its supporting infrastructure.

The project uses containerized services for components such as:

```text
Django
PostgreSQL
Redis
Celery
```

This makes the local environment more reproducible and reduces dependency setup differences between machines.

---

## 🧪 Testing

Tests can be executed using the project's configured test setup.

```bash
pytest
```

The test suite is also integrated into the project's CI workflow.

---

## 🔄 CI/CD

PRSentinel uses **GitHub Actions** for automated validation.

The workflow runs automatically for relevant repository events and executes the project's tests against the application environment.

```text
Git Push / Pull Request
          ↓
    GitHub Actions
          ↓
    Setup Environment
          ↓
      Run Tests
          ↓
    Build / Validation
```

---

## 📸 Example

A typical PRSentinel workflow looks like:

```text
Developer creates Pull Request
              ↓
       GitHub Webhook
              ↓
        Django Backend
              ↓
       Celery + Redis
              ↓
        LLM Code Review
              ↓
       Review Findings
              ↓
      GitHub Inline Comments
```

---

## 🎯 Why PRSentinel?

Modern development workflows increasingly rely on AI-assisted coding.

As code generation becomes faster, the amount of code requiring review can increase as well.

PRSentinel explores how AI can be integrated into the existing software development workflow to make code review:

* Faster
* Automated
* Consistent
* Integrated directly into GitHub
* Less dependent on manual first-pass review

The project also serves as an exploration of building an AI-powered feature on top of a production-style backend architecture rather than treating the LLM as a standalone script.

---

## 📚 Key Engineering Concepts

Building PRSentinel provided hands-on experience with:

* Django backend architecture
* REST APIs
* GitHub Webhooks
* GitHub REST API integration
* Asynchronous task processing
* Celery
* Redis
* PostgreSQL
* Docker
* Docker Compose
* CI/CD with GitHub Actions
* LLM API integration
* Automated code analysis

---

## 🔮 Future Improvements

Potential future improvements include:

* [ ] Support for multiple LLM providers
* [ ] Configurable review rules
* [ ] Review severity levels
* [ ] Improved duplicate finding detection
* [ ] Review analytics dashboard
* [ ] More granular repository-level configuration

---

## 👨‍💻 Author

**Achiv Gupta**

Built as a backend + AI engineering project to explore how LLM-powered code review can be integrated into a real software development workflow.

---

## ⭐ If You Find It Interesting

If you find the project useful or interesting, consider giving the repository a ⭐ and exploring the implementation.
