import os
import sys
import requests
from lxml import html

GITHUB_TOKEN = os.getenv("GH_TOKEN")
PR_NUMBER = os.getenv("PR_NUMBER")  # We'll set this via workflow env
REPO = os.getenv("GITHUB_REPOSITORY")

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

def get_names_from_readme(readme_path):
    with open(readme_path, "r", encoding="utf-8") as file:
        readme_content = file.read()

    tree = html.fromstring(readme_content)
    table = tree.xpath('//table')[0]
    rows = table.xpath('.//tr')
    names = []

    for row_index, row in enumerate(rows):
        cols = row.xpath('.//td')
        if len(cols) == 7:
            for col_index, col in enumerate(cols):
                name_element = col.xpath('.//b')
                if name_element:
                    name = name_element[0].text.strip()
                    line_num = name_element[0].sourceline
                    names.append((name, line_num))
    return names

def main():
    base_names = get_names_from_readme("README.md")
    head_names = get_names_from_readme("head/README.md")

    head_name_dict = {name: line_num for name, line_num in head_names}
    if len(head_name_dict) != len(head_names):
        comment_on_pr("❌ Duplicate names detected in the contributor table. Please ensure each name appears only once.")
        sys.exit(1)

    added_names = list(set(head_name_dict.keys()) - set(name for name, _ in base_names))
    if len(added_names) != 1:
        comment_on_pr("❌ Only one contributor should be added per pull request.")
        sys.exit(1)

    added_name = added_names[0]
    if added_name != head_names[-1][0]:
        comment_on_pr(f"❌ Contributor name should be added at the end of the table. Please move `{added_name}` to the last cell.")
        sys.exit(1)

    tree = html.fromstring(open("head/README.md", "r", encoding="utf-8").read())
    table = tree.xpath('//table')[0]
    rows = table.xpath('.//tr')

    for row in rows:
        cols = row.xpath('.//td')
        if len(cols) > 7:
            comment_on_pr(f"❌ Too many columns in a row. Each row should have max 7 contributors.")
            sys.exit(1)

    comment_on_pr("✅ Validation passed! Thanks for contributing 💫")

if __name__ == "__main__":
    main()
