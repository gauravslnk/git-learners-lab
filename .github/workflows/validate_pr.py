import os
import sys
import requests
from lxml import html

GITHUB_TOKEN = os.getenv("GH_TOKEN")
PR_NUMBER = os.getenv("PR_NUMBER")
REPO = os.getenv("GITHUB_REPOSITORY")


def get_modified_files():
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch PR files: {response.status_code}, {response.text}")
        sys.exit(1)
    return [file["filename"] for file in response.json()]


def comment_on_pr(message):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.post(url, headers=headers, json={"body": message})
    if response.status_code != 201:
        print(f"⚠️ Failed to comment on PR: {response.status_code}, {response.text}")


def label_on_pr(label):
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/labels"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.post(url, headers=headers, json={"labels": [label]})
    if response.status_code != 200:
        print(f"⚠️ Failed to label PR: {response.status_code}, {response.text}")


def get_names_from_readme(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        tree = html.fromstring(content)
        table = tree.xpath('//table')[0]
    except Exception as e:
        print(f"❌ Failed to parse table from {readme_path}: {e}")
        return []

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
    print("📄 Validating README changes...")

    base_names = get_names_from_readme("base/README.md")
    head_names = get_names_from_readme("head/README.md")

    print("📋 Base names:", [name for name, _ in base_names])
    print("📋 Head names:", [name for name, _ in head_names])

    head_name_dict = {name: line_num for name, line_num in head_names}
    if len(head_name_dict) != len(head_names):
        fail("Duplicate names detected in the contributor table. Please ensure each name appears only once.")

    added_names = list(set(head_name_dict.keys()) - set(name for name, _ in base_names))
    if len(added_names) != 1:
        fail("Only one contributor should be added per pull request.")

    added_name = added_names[0]
    if added_name != head_names[-1][0]:
        fail(f"Contributor name should be added at the end of the table. Please move `{added_name}` to the last cell.")

    try:
        tree = html.fromstring(open("head/README.md", "r", encoding="utf-8").read())
        table = tree.xpath('//table')[0]
        rows = table.xpath('.//tr')
        for row in rows:
            cols = row.xpath('.//td')
            if len(cols) > 7:
                fail("Too many columns in a row. Each row should have max 7 contributors.")
    except Exception as e:
        fail(f"❌ Unable to validate table structure: {e}")

    comment_on_pr("✅ Validation passed! Thanks for contributing 💫")
    label_on_pr("✅ passed")


if __name__ == "__main__":
    main()
