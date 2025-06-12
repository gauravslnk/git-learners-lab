import os
import sys
import requests
from bs4 import BeautifulSoup
import markdown

GITHUB_TOKEN = os.getenv("GH_TOKEN")
PR_NUMBER = os.getenv("PR_NUMBER")
REPO = os.getenv("GITHUB_REPOSITORY")

def api_get(url):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    return requests.get(url, headers=headers)

def api_post(url, json_data):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    return requests.post(url, headers=headers, json=json_data)

def comment_on_pr(message):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    api_post(url, {"body": message})

def label_on_pr(label):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/labels"
    api_post(url, {"labels": [label]})

def fail(message):
    comment_on_pr(f"❌ {message}")
    label_on_pr("❌ failed")
    sys.exit(1)

def parse_names_from_readme(path):
    with open(path, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = markdown.markdown(md_content, extensions=['tables'])
    soup = BeautifulSoup(html_content, "html.parser")

    table = soup.find("table")
    if not table:
        fail(f"No table found in {path}. Please ensure you're using a valid Markdown table.")

    names = []
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) == 7:
            for col in cols:
                bold = col.find("strong") or col.find("b")
                if bold:
                    names.append((bold.get_text(strip=True), None))
    return names

def main():
    print("📄 Validating README.md contributor table...")

    base_names = parse_names_from_readme("base/README.md")
    head_names = parse_names_from_readme("head/README.md")

    print("✅ Base names:", [n for n, _ in base_names])
    print("✅ Head names:", [n for n, _ in head_names])

    head_name_dict = {name: idx for idx, (name, _) in enumerate(head_names)}

    if len(head_name_dict) != len(head_names):
        fail("Duplicate contributor names found. Each contributor must be unique.")

    added_names = list(set(head_name_dict) - set(n for n, _ in base_names))
    if len(added_names) != 1:
        fail("Only one new contributor can be added per pull request.")

    added_name = added_names[0]
    if added_name != head_names[-1][0]:
        fail(f"Contributor `{added_name}` must be added at the end of the table.")

    # Validate max 7 per row
    soup = BeautifulSoup(markdown.markdown(open("head/README.md", encoding="utf-8").read(), extensions=["tables"]), "html.parser")
    for row in soup.find_all("tr"):
        if len(row.find_all("td")) > 7:
            fail("Each row can have a maximum of 7 contributors.")

    comment_on_pr("✅ Validation passed! Thanks for contributing 💫")
    label_on_pr("✅ passed")

if __name__ == "__main__":
    main()
