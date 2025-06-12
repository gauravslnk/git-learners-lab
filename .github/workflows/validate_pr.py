import os
import sys
import requests
from bs4 import BeautifulSoup
import markdown

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
    if method == "GET":
        return requests.get(url, headers=headers)
    else:
        return requests.post(url, headers=headers, json=json_data)

def comment_on_pr(message):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    github_api_request(url, "POST", {"body": message})

def label_pr(label):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/labels"
    github_api_request(url, "POST", {"labels": [label]})

def fail(message):
    print(f"[FAIL] {message}")
    comment_on_pr(f"❌ Validation failed: {message}")
    label_pr(FAILURE_LABEL)
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
            contributors.append(name_tag.get_text(strip=True))
    return contributors

# Row structure checker
def validate_table_structure():
    with open("head/README.md", "r", encoding="utf-8") as f:
        html = markdown.markdown(f.read(), extensions=["tables"])
    
    soup = BeautifulSoup(html, "html.parser")
    for row in soup.find_all("tr"):
        if len(row.find_all("td")) > 7:
            fail("Each row must contain no more than 7 contributors")

# Main logic
def main():
    print("🚀 Starting PR validation...")

    try:
        base_contributors = parse_contributors("base/README.md")
        head_contributors = parse_contributors("head/README.md")
    except Exception as e:
        fail(f"Error parsing README: {str(e)}")

    print(f"Base contributors: {base_contributors}")
    print(f"Head contributors: {head_contributors}")

    # Check for duplicate names
    if len(head_contributors) != len(set(head_contributors)):
        fail("Duplicate contributor names found")

    # Ensure exactly one new contributor added
    new_contributors = set(head_contributors) - set(base_contributors)
    if len(new_contributors) != 1:
        fail("Exactly one new contributor must be added per PR")

    # Check contributor is added at the end
    new_contributor = new_contributors.pop()
    if head_contributors[-1] != new_contributor:
        fail(f"New contributor '{new_contributor}' must be added at the end of the table")

    # Validate row structure
    validate_table_structure()

    # All good!
    comment_on_pr("✅ Validation passed! Your contribution will be merged automatically. 💫")
    label_pr(SUCCESS_LABEL)
    print("✅ Validation completed successfully.")

if __name__ == "__main__":
    main()
