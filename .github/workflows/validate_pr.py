import os
import sys
import requests
from bs4 import BeautifulSoup
import markdown
import re

# Environment variables
GITHUB_TOKEN = os.getenv("GH_TOKEN")
PR_NUMBER = os.getenv("PR_NUMBER")
REPO = os.getenv("GITHUB_REPOSITORY")

# Label constants
SUCCESS_LABEL = "✅ passed"
FAILURE_LABEL = "❌ failed"

# GitHub API utility
def github_api_request(url, method="GET", json_data=None):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        else:
            response = requests.post(url, headers=headers, json=json_data)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API request failed: {str(e)}", file=sys.stderr)
        return None

def comment_on_pr(message):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    return github_api_request(url, "POST", {"body": message})

def manage_pr_labels(label):
    # First remove any existing validation labels
    github_api_request(
        f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/labels/{FAILURE_LABEL}",
        "DELETE"
    )
    github_api_request(
        f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/labels/{SUCCESS_LABEL}",
        "DELETE"
    )
    
    # Add the new label
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/labels"
    return github_api_request(url, "POST", {"labels": [label]})

def fail(message):
    print(f"[FAIL] {message}", file=sys.stderr)
    comment_on_pr(f"❌ Validation failed: {message}")
    manage_pr_labels(FAILURE_LABEL)
    sys.exit(1)

def success():
    print("[SUCCESS] All checks passed", file=sys.stderr)
    comment_on_pr("✅ Validation passed! Your contribution will be merged automatically. 💫")
    manage_pr_labels(SUCCESS_LABEL)
    sys.exit(0)

def validate_contributor_table(readme_path):
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            md_content = f.read()
    except FileNotFoundError:
        fail(f"README.md not found at {readme_path}")

    # Convert markdown to HTML
    html = markdown.markdown(md_content, extensions=["tables"])
    soup = BeautifulSoup(html, "html.parser")

    # Verify table exists
    table = soup.find("table")
    if not table:
        fail("Contributor table not found in README.md")

    contributors = []
    for row in table.find_all("tr")[1:]:  # Skip header row
        cells = row.find_all("td")
        if len(cells) > 7:
            fail("Maximum 7 contributors allowed per row")
            
        for cell in cells:
            name_tag = cell.find("b")
            if not name_tag:
                fail("Each contributor must be wrapped in <b> tags")
                
            name = name_tag.get_text(strip=True)
            if not re.match(r"^[a-zA-Z0-9_. -]+$", name):
                fail(f"Invalid name format: '{name}'. Only letters, numbers, spaces, dots, underscores and hyphens allowed")
                
            contributors.append(name)
            
    return contributors

def main():
    print("🚀 Starting PR validation...", file=sys.stderr)

    try:
        # Get contributors from both versions
        old_contributors = validate_contributor_table("base/README.md")
        new_contributors = validate_contributor_table("head/README.md")
        
        print(f"Current contributors: {len(old_contributors)}", file=sys.stderr)
        print(f"Updated contributors: {len(new_contributors)}", file=sys.stderr)

        # Check for duplicates
        if len(new_contributors) != len(set(new_contributors)):
            fail("Duplicate contributor names found")

        # Check what changed
        added = set(new_contributors) - set(old_contributors)
        removed = set(old_contributors) - set(new_contributors)

        # Validate changes
        if len(added) == 1 and not removed:
            # Simple addition case
            new_name = added.pop()
            if new_contributors[-1] != new_name:
                fail(f"New contributor '{new_name}' must be added at the end")
        elif len(added) == 1 and len(removed) == 1:
            # Name correction case
            old_name = removed.pop()
            new_name = added.pop()
            if new_contributors.count(new_name) > 1:
                fail("Name correction would create duplicate entries")
        else:
            fail("Each PR must either:\n- Add exactly one new contributor\n- Correct exactly one existing name")

        # All checks passed
        success()

    except Exception as e:
        fail(f"Unexpected error during validation: {str(e)}")

if __name__ == "__main__":
    main()
