import os
import sys
import requests
from lxml import html

GITHUB_TOKEN = os.getenv("GH_TOKEN")
PR_NUMBER = os.getenv("PR_NUMBER")
REPO = os.getenv("GITHUB_REPOSITORY")

def get_modified_files():
    """Get the list of files modified in the PR."""
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch PR files: {response.status_code}, {response.text}")
        sys.exit(1)

    files = response.json()
    return [file["filename"] for file in files]


def comment_on_pr(message):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    data = {"body": message}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 201:
        print(f"⚠️ Failed to comment on PR: {response.status_code}, {response.text}")

def label_on_pr(label):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/labels"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    data = {"labels": [label]}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"⚠️ Failed to label PR: {response.status_code}, {response.text}")

def get_names_from_readme(readme_path):
    with open(readme_path, "r", encoding="utf-8") as file:
        readme_content = file.read()

    tree = html.fromstring(readme_content)
    table = tree.xpath('//table')[0]
    rows = table.xpath('.//tr')
    names = []

    for row in rows:
        cols = row.xpath('.//td')
        if len(cols) == 7:
            for col in cols:
                name_element = col.xpath('.//b')
                if name_element:
                    name = name_element[0].text.strip()
                    line_num = name_element[0].sourceline
                    names.append((name, line_num))
    return names

def fail(message):
    comment_on_pr(f"❌ {message}")
    label_on_pr("❌ failed")
    sys.exit(1)

def main():
    base_names = get_names_from_readme("README.md")
    head_names = get_names_from_readme("head/README.md")

    modified_files = get_modified_files()
    print("📂 Files changed in this PR:", modified_files)

    non_readme_files = [f for f in modified_files if f != "README.md"]
    if non_readme_files:
        fail(
            f"You can only modify `README.md` in this repository.\n\n"
            f"🚫 Detected changes in: `{', '.join(non_readme_files)}`\n\n"
            "Please revert those changes and try again. This repo is meant for contributors to update only the contributors table."
        )


    head_name_dict = {name: line_num for name, line_num in head_names}
    if len(head_name_dict) != len(head_names):
        fail("Duplicate names detected in the contributor table. Please ensure each name appears only once.")

    added_names = list(set(head_name_dict.keys()) - set(name for name, _ in base_names))
    if len(added_names) != 1:
        fail("Only one contributor should be added per pull request.")

    added_name = added_names[0]
    if added_name != head_names[-1][0]:
        fail(f"Contributor name should be added at the end of the table. Please move `{added_name}` to the last cell.")

    tree = html.fromstring(open("head/README.md", "r", encoding="utf-8").read())
    table = tree.xpath('//table')[0]
    rows = table.xpath('.//tr')
    for row in rows:
        cols = row.xpath('.//td')
        if len(cols) > 7:
            fail("Too many columns in a row. Each row should have max 7 contributors.")

    comment_on_pr("✅ Validation passed! Thanks for contributing 💫")
    label_on_pr("✅ passed")

if __name__ == "__main__":
    main()
