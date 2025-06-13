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
        "Accept": "application/vnd.github+json"
    }
    try:
        if method == "GET":
            r = requests.get(url, headers=headers)
        else:
            r = requests.post(url, headers=headers, json=json_data)
        r.raise_for_status()
        return r
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API request failed: {str(e)}")
        return None

def comment_on_pr(message):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    return github_api_request(url, "POST", {"body": message})

def label_pr(label):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/labels"
    return github_api_request(url, "POST", {"labels": [label]})

def fail(message):
    print(f"[FAIL] {message}")
    try:
        comment_on_pr(f"❌ Validation failed: {message}")
        label_pr(FAILURE_LABEL)
    except:
        print("Warning: Could not post comment or label - continuing anyway")
    sys.exit(1)

# Contributor parser
def parse_contributors(readme_path):
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            md_content = f.read()
    except FileNotFoundError:
        fail(f"README.md not found at {readme_path}")

    html = markdown.markdown(md_content, extensions=["tables"])
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")
    if not table:
        fail("Contributor table not found in README.md")

    contributors = []
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        for cell in cells:
            name_tag = cell.find("b")
            if not name_tag:
                fail("Each contributor name must be enclosed in <b> tags")
            name = name_tag.get_text(strip=True)
            if not re.match(r"^[\w\s\-\.]{1,39}$", name):  # Updated regex
                fail(f"Invalid name format: '{name}'")
            contributors.append(name)
    return contributors

# Row structure checker
def validate_table_structure():
    with open("head/README.md", "r", encoding="utf-8") as f:
        html = markdown.markdown(f.read(), extensions=["tables"])
    
    soup = BeautifulSoup(html, "html.parser")
    for i, row in enumerate(soup.find_all("tr")):
        cells = row.find_all("td")
        if len(cells) > 7:
            fail(f"Row {i+1} has more than 7 contributors ({len(cells)} found)")

def main():
    print("🚀 Starting PR validation...")

    try:
        base_contributors = parse_contributors("base/README.md")
        head_contributors = parse_contributors("head/README.md")
    except Exception as e:
        fail(f"Error parsing README: {str(e)}")

    print(f"Base contributors: {base_contributors}")
    print(f"Head contributors: {head_contributors}")

    # Check for duplicates
    if len(head_contributors) != len(set(head_contributors)):
        fail("Duplicate contributor names found")

    # Ensure exactly one contributor added
    new_contributors = set(head_contributors) - set(base_contributors)
    if len(new_contributors) != 1:
        fail("Exactly one new contributor must be added per PR")

    # Ensure contributor is at the end
    new_contributor = new_contributors.pop()
    if head_contributors[-1] != new_contributor:
        fail(f"New contributor '{new_contributor}' must be added at the end of the table")

    # Validate table structure
    validate_table_structure()

    # All good!
    try:
        comment_on_pr("✅ Validation passed! Your contribution will be merged automatically. 💫")
        label_pr(SUCCESS_LABEL)
    except:
        print("Warning: Could not post success comment - continuing anyway")
    print("✅ Validation completed successfully.")

if __name__ == "__main__":
    main()
