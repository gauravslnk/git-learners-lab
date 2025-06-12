# 🌱 Welcome to git-learners-lab – Contributor Guide

> A complete, beginner-friendly guide to help you make your **first open-source contribution** via GitHub – even if you’ve never used Git before!

---

## ✅ Prerequisites (Only Once)

Before contributing, please:

- 🔧 [Install Git](https://git-scm.com/downloads)
- 🧑‍💻 Create a GitHub account (if you don’t already have one)
- 💡 Optional: Install [VS Code](https://code.visualstudio.com/) as your code editor

To verify Git installation, run:

```bash
git --version
````

You should see something like `git version 2.xx.x`

---

## 📜 Contribution Rules

To maintain consistency and keep things easy to review:

* ✅ Add **only one contributor** per Pull Request (PR)
* ✅ Add your card **at the end** of the contributors list
* ✅ Do **not duplicate** existing entries
* ✅ Each row can have a **maximum of 7 cards**
* ✅ Only modify `README.md` (unless you’re fixing another issue)

---

> 💡 Tip: Use `Ctrl + Shift + V` in VS Code to preview the `README.md` before committing.

---

## 📝 Step-by-Step Guide to Contribute

---

### 🔁 1. Fork This Repository

Head to the main repo:
👉 [https://github.com/gauravslnk/git-learners-lab](https://github.com/gauravslnk/git-learners-lab)

Click the **Fork** button (top-right), then select your GitHub account.

---

### 💻 2. Clone Your Fork

Open your terminal / Git Bash and run:

```bash
git clone https://github.com/<your-username>/git-learners-lab.git
cd git-learners-lab
```

---

### 🌿 3. Create a New Branch

```bash
git checkout -b add-your-name
```

This keeps your changes separate and organized.

---

### ✨ 4. Add Yourself to the Contributors Table

1. Open the project in VS Code:

```bash
code .
```

2. Open `README.md`
3. Scroll to the section between:

```html
<!-- ALL-CONTRIBUTORS-LIST:START -->
...
<!-- ALL-CONTRIBUTORS-LIST:END -->
```

4. At the end of the last row (or start a new row if needed), add this block:

```html
<td align="center">
  <a href="https://github.com/your-username">
    <img src="https://avatars.githubusercontent.com/your-id" width="100px;" alt="Your Name" />
    <br />
    <sub><b>Your Name</b></sub>
  </a>
</td>
```

#### 🔁 Replace:

| Placeholder     | Replace with                                               |
| --------------- | ---------------------------------------------------------- |
| `your-username` | Your GitHub username                                       |
| `your-id`       | Your GitHub avatar ID *(Right-click → Copy image address)* |
| `Your Name`     | Your actual name                                           |

✅ Ensure your card is at the **end** of the list.

---

### 💾 5. Save & Commit Your Changes

```bash
git add README.md
git commit -m "Added <Your Name> to contributors list"
```

---

### 🚀 6. Push Your Branch to GitHub

```bash
git push origin add-your-name
```

---

### 🔃 7. Create a Pull Request (PR)

1. Go to your fork on GitHub
2. Click the `Compare & pull request` button
3. Use a title like:

```text
Added My Name to Contributors List ✨
```

4. Click **Create pull request**

---

### 🤖 8. Let the Bot Validate Your PR

Wait a few seconds...

#### ✅ If successful:

* Green checkmark ✅ on the PR
* Bot comments: `"✅ Validation passed! Thanks for contributing 💫"`

#### ❌ If failed:

* Red ❌ checkmark
* Bot comments with what went wrong (e.g. wrong position, duplicate)

Fix it, commit again, and push — no need to open a new PR.

---

### 🎉 9. Celebrate!

Boom! You’ve just:

* ✅ Forked a repo
* ✅ Cloned it locally
* ✅ Created a branch
* ✅ Edited a file
* ✅ Made a PR
* ✅ Passed bot validation
* ✅ Made your first open-source contribution!

---

## 📚 Want to Learn More?

Check out this beginner-friendly resource:

📘 [Chai aur Git - Docs](https://docs.chaicode.com/youtube/chai-aur-git/introduction/)

---

## ❤️ Thank You!

Thanks for joining the community and contributing to **git-learners-lab**. We’re excited to have you here — and hope this was the start of many open-source adventures ahead 🚀

For any help, feel free to:

* Ask in the DSC group
* Or [Open an Issue](https://github.com/gauravslnk/git-learners-lab/issues)

---
