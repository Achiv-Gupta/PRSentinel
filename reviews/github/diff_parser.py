import re


def parse_patch(patch):
    """
    Convert a GitHub patch into changed lines with
    their new-file line numbers and diff positions.
    """

    results = []

    new_line = None
    position = 0

    for raw_line in patch.splitlines():

        position += 1

        if raw_line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", raw_line)

            if match:
                new_line = int(match.group(1))

            continue

        if new_line is None:
            continue

        if raw_line.startswith("+") and not raw_line.startswith("+++"):
            content = raw_line[1:]

            results.append({
                "content": content,
                "line": new_line,
                "position": position,
            })

            new_line += 1

        elif raw_line.startswith("-") and not raw_line.startswith("---"):
            continue

        else:
            new_line += 1

    return results

def find_issue_location(patch, line_content):

    changed_lines = parse_patch(patch)

    for changed_line in changed_lines:
        if changed_line["content"].strip() == line_content.strip():
            return changed_line

    return None