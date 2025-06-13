import os
import sys
import requests
from bs4 import BeautifulSoup
import markdown
import re
import urllib.parse

# Environment variables
GITHUB_TOKEN = os.getenv("GH_TOKEN")
PR_NUMBER = os.getenv("PR_NUMBER")
REPO = os.getenv("GITHUB_REPOSITORY")

# Label constants
SUCCESS_LABEL = "passed"
FAILURE_LABEL = "failed"
EMOJI_SUCCESS = "✅"
EMOJI_FAILURE = "❌"

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
        print(f"[API ERROR] {method} {url}: {str(e)}", file=sys.stderr)
        return None

def comment_on_pr(message):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    return github_api_request(url, "POST", {"body": message})

def manage_pr_labels(label, emoji):
    # URL encode the label
    encoded_label = urllib.parse.quote(label)
    full_label = f"{emoji} {label}"
    
    # Remove opposite label first
    opposite_label = FAILURE_LABEL if label == SUCCESS_LABEL else SUCCESS_LABEL
    github_api_request(
        f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/labels/{urllib.parse.quote(opposite_label)}",
        "DELETE"
    )
    
    # Add the new label
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/labels"
    return github_api_request(url, "POST", {"labels": [full_label]})

def fail(message):
    print(f"[VALIDATION FAILED] {message}", file=sys.stderr)
    try:
        comment_on_pr(f"{EMOJI_FAILURE} Validation failed: {message}")
        manage_pr_labels(FAILURE_LABEL, EMOJI_FAILURE)
    except Exception as e:
        print(f"[ERROR] Failed to update PR: {str(e)}", file=sys.stderr)
    sys.exit(1)

def success():
    print("[VALIDATION SUCCESS] All checks passed", file=sys.stderr)
    try:
        comment_on_pr(f"{EMOJI_SUCCESS} Validation passed! Your PR will be auto-merged.")
        manage_pr_labels(SUCCESS_LABEL, EMOJI_SUCCESS)
    except Exception as e:
        print(f"[WARNING] Failed to update PR: {str(e)}", file=sys.stderr)
    sys.exit(0)

def validate_contributor_table(readme_path):
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            md_content = f.read().strip()
            
        if not md_content:
            return []
            
        html = markdown.markdown(md_content, extensions=["tables"])
        soup = BeautifulSoup(html, "html.parser")

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
                if not re.match(r"^[\w\s\-.]{1,50}$", name):
                    fail(f"Invalid name format: '{name}'. Only letters, numbers, spaces, hyphens and dots allowed")
                    
                contributors.append(name)
                
        return contributors

    except Exception as e:
        fail(f"Error parsing {readme_path}: {str(e)}")

def main():
    print("🚀 Starting PR validation...", file=sys.stderr)

    try:
        old_contributors = validate_contributor_table("base/README.md")
        new_contributors = validate_contributor_table("head/README.md")
        
        if not old_contributors and not new_contributors:
            fail("README.md appears empty. Please add a contributors table.")
            
        print(f"Current contributors: {len(old_contributors)}", file=sys.stderr)
        print(f"Updated contributors: {len(new_contributors)}", file=sys.stderr)

        # Check for duplicates
        if len(new_contributors) != len(set(new_contributors)):
            fail("Duplicate contributor names found")

        added = set(new_contributors) - set(old_contributors)
        removed = set(old_contributors) - set(new_contributors)

        # Validation cases
        if len(added) == 1 and not removed:
            new_name = added.pop()
            if new_contributors[-1] != new_name:
                fail(f"New contributor '{new_name}' must be added at the end")
        elif len(added) == 1 and len(removed) == 1:
            old_name = removed.pop()
            new_name = added.pop()
            if new_contributors.count(new_name) > 1:
                fail("Name correction would create duplicate entries")
        else:
            fail("Each PR must either:\n- Add exactly one new contributor\n- Correct exactly one existing name")

        success()

    except Exception as e:
        fail(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
