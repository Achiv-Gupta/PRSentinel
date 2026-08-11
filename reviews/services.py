from .github.client import GitHubClient
from .github.diff_parser import find_issue_location
from .llm.client import LLMClient


def process_pull_request(repo, pr_number):

    github = GitHubClient()
    llm = LLMClient()

    # 1. Get PR information
    pr = github.get_pull_request(repo, pr_number)

    # 2. Get changed files
    files = github.get_pull_request_files(
        repo,
        pr_number
    )

    # 3. Run AI review
    review_result = llm.review_code(
        repo,
        pr["title"],
        files
    )

    # 4. Filter low-confidence issues
    issues = filter_issues(review_result)

    # 5. Process each issue
    for issue in issues:

        # Find the matching file
        file_data = next(
            (
                file
                for file in files
                if file["filename"] == issue.file
            ),
            None
        )

        if not file_data:
            continue

        # Find exact location in diff
        location = find_issue_location(
            file_data["patch"],
            issue.line_content
        )

        if not location:
            print(
                f"Could not locate issue in diff: "
                f"{issue.file}"
            )
            continue

        # Build GitHub comment
        body = (
            f"**{issue.severity.upper()} {issue.issue_type.upper()}**\n\n"
            f"{issue.description}\n\n"
            f"**Suggestion:** {issue.suggestion}\n\n"
            f"_Confidence: {issue.confidence:.0%}_"
        )

        # Post comment
        github.create_review_comment(
            repo=repo,
            pr_number=pr_number,
            body=body,
            commit_id=pr["head"]["sha"],
            path=issue.file,
            line=location["line"],
        )

        print(
            f"Posted review for {issue.file}:{location['line']}"
        )

CONFIDENCE_THRESHOLD = 0.80


def filter_issues(review_result):
    return [
        issue
        for issue in review_result.issues
        if issue.confidence >= CONFIDENCE_THRESHOLD
    ]