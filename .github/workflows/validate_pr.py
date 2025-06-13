import os
import re
import sys
from github import Github

# Initialize GitHub instance
g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(os.getenv("GITHUB_REPOSITORY"))

# Get the pull request
pr = repo.get_pull(int(os.getenv("GITHUB_PR_NUMBER")))

# Check if only README.md is modified
def check_files_changed(pr):
    files = pr.get_files()
    for file in files:
        if file.filename != "README.md":
            return False
    return True

# Check if the contributor is added at the end
def check_contributor_addition(pr):
    files = pr.get_files()
    for file in files:
        if file.filename == "README.md":
            # Fetch the content of the README.md file
            contents = repo.get_contents("README.md")
            readme_content = contents.decoded_content.decode()

            # Check if the PR author is added at the end
            pattern = re.compile(r'<td align="center">\s*<a href="https://github\.com/' + pr.user.login + r'">\s*<img.*?/\s*>\s*<br\s*/?>\s*<sub><b>' + re.escape(pr.user.login) + r'<\/b><\/sub>\s*<\/a>\s*<\/td>')
            matches = pattern.findall(readme_content)

            if not matches:
                return False

            # Check if the addition is at the end
            last_match_position = readme_content.rfind(matches[-1])
            if last_match_position == -1 or last_match_position + len(matches[-1]) != len(readme_content.strip()):
                return False

    return True

# Validate PR
if not check_files_changed(pr):
    pr.create_issue_comment("❌ Validation failed: Only README.md should be modified.")
    sys.exit(1)

if not check_contributor_addition(pr):
    pr.create_issue_comment("❌ Validation failed: Contributor not added correctly at the end.")
    sys.exit(1)

# Auto-merge the PR if validations pass
pr.create_issue_comment("✅ Validation passed! Thanks for contributing 💫")
pr.merge(merge_method='squash')
