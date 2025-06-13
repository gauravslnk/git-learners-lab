import os
import re
import sys
from github import Github
from github.GithubException import GithubException

# Initialize GitHub API
g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(os.getenv("GITHUB_REPOSITORY"))
pr = repo.get_pull(int(os.getenv("GITHUB_PR_NUMBER")))

def check_files_changed(pr):
    files = pr.get_files()
    for file in files:
        if file.filename != "README.md":
            return False
    return True

def check_contributor_addition(pr):
    try:
        contents = repo.get_contents("README.md", ref=pr.head.sha)
        readme = contents.decoded_content.decode().strip()
    except GithubException as e:
        pr.create_issue_comment(f"❌ Error reading README.md: {e}")
        return False

    username = pr.user.login

    # Regex pattern to match contributor card
    pattern = re.compile(
        rf'<td align="center">\s*<a href="https://github\.com/{re.escape(username)}">\s*<img.*?>\s*<br\s*/?>\s*<sub><b>{re.escape(username)}</b></sub>\s*</a>\s*</td>',
        re.IGNORECASE | re.DOTALL
    )

    matches = list(pattern.finditer(readme))

    if not matches:
        return False

    last_match = matches[-1]
    # Check that the last contributor card is at the end of the file (after trimming trailing whitespace)
    if not readme.rstrip().endswith(readme[last_match.start():last_match.end()]):
        return False

    return True

def check_max_seven_per_row(pr):
    try:
        contents = repo.get_contents("README.md", ref=pr.head.sha)
        readme = contents.decoded_content.decode()
    except GithubException as e:
        pr.create_issue_comment(f"❌ Error reading README.md for row validation: {e}")
        return False

    # Count <td> tags between each <tr>
    rows = re.findall(r'<tr>(.*?)</tr>', readme, re.DOTALL)
    for i, row in enumerate(rows):
        td_count = len(re.findall(r'<td\s+align="center">', row))
        if td_count > 7:
            pr.create_issue_comment(f"❌ Validation failed: Row {i+1} has more than 7 contributor cards. Please limit to 7 per row.")
            return False
    return True

# Run validations
if not check_files_changed(pr):
    pr.create_issue_comment("❌ Validation failed: Only `README.md` should be modified.")
    sys.exit(1)

if not check_contributor_addition(pr):
    pr.create_issue_comment("❌ Validation failed: Contributor not added correctly or not at the end of the list.")
    sys.exit(1)

if not check_max_seven_per_row(pr):
    sys.exit(1)

# All validations passed
pr.create_issue_comment("✅ Validation passed! Thanks for contributing 💫")
pr.merge(merge_method='squash')
