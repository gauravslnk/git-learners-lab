# 🌱 Welcome to Git Learners Lab – Contributor Guide

> A beginner-friendly, step-by-step guide to help you make your **first open-source contribution** – even if you’ve never used Git before!

---

## ✅ Prerequisites (One-time Setup)

Before contributing, please ensure:

- 🔧 [Git is installed](https://git-scm.com/downloads)
- 🧑‍💻 You have a GitHub account
- 💡 (Optional) [VS Code installed](https://code.visualstudio.com/) as your editor

Check Git installation:

```bash
git --version
````

You should see something like `git version 2.xx.x`.

---

## 📜 Contribution Rules & Guidelines

To keep contributions consistent and the project beginner-friendly:

### ✅ Do:

* Add **only one contributor card per PR**
* Place your card **at the end** of the contributors list
* Follow the correct **HTML format** (card template below)
* Start a new row only **after 7 cards** in the previous row
* Modify **only the `README.md`** file

### ❌ Don't:

* Edit or delete any other content in `README.md`
* Change any other file in the repo
* Add more than one card per PR
* Insert your card in the middle or top of the list
* Create multiple PRs for the same change

> ⚠️ PRs violating these rules will be automatically rejected by the GitHub bot.

---

## 📝 How to Contribute – Step-by-Step

---

### 🔁 1. Fork This Repository

Go to:
👉 [https://github.com/gauravslnk/git-learners-lab](https://github.com/gauravslnk/git-learners-lab)

Click **Fork** (top right corner), and choose your GitHub account.

---

### 💻 2. Clone Your Fork Locally

```bash
git clone https://github.com/<your-username>/git-learners-lab.git
cd git-learners-lab
```

---

### 🌿 3. Create a New Branch

```bash
git checkout -b add-your-username
```

---

### ✨ 4. Add Your Contributor Card

1. Open the project folder in VS Code:

```bash
code .
```

2. Open `README.md`
3. Scroll to the section marked:

```html
<!-- ALL-CONTRIBUTORS-LIST:START -->
...
<!-- ALL-CONTRIBUTORS-LIST:END -->
```

4. Find the **last row** of contributors (each row has up to 7 cards).
5. At the end of the row, or in a new row if needed, add this block:

```html
<td align="center">
  <a href="https://github.com/your-username">
    <img src="https://avatars.githubusercontent.com/your-id" width="100px;" alt="Your User Name" />
    <br />
    <sub><b>Your User Name</b></sub>
  </a>
</td>
```

#### Replace placeholders:

| Placeholder      | Replace with                                               |
| ---------------- | ---------------------------------------------------------- |
| `your-username`  | Your GitHub username                                       |
| `your-id`        | Your avatar image ID (Right-click avatar → Copy image URL) |
| `Your User Name` | Your User name                                             |

✅ Make sure your card:

* Is added **at the end**
* **Follows the format exactly**
* **Starts a new row** if you're the 8th contributor

---

### 💾 5. Save, Add, Commit

```bash
git add README.md
git commit -m "Added <Your User Name> to contributors list"
```

---

### 🚀 6. Push Your Branch

```bash
git push origin add-your-username
```

---

### 🔃 7. Create a Pull Request (PR)

1. Visit your fork on GitHub
2. Click **Compare & pull request**
3. Use a title like:

```text
Added My Name to Contributors List ✨
```

4. Click **Create pull request**

---

### 🤖 8. Let the Bot Validate Your PR

Once submitted, the GitHub bot will check your PR automatically.

#### ✅ If it passes:

* PR gets auto-merged 🥳
* You’ll see: `✅ Validation passed! Thanks for contributing 💫`

#### ❌ If it fails:

* You'll get a comment explaining what went wrong (e.g., wrong file, not last, over 7 per row)
* Fix your code and push again — no need to reopen PR

---

### 🎉 9. Celebrate!

You’ve just:
✅ Forked a repo
✅ Cloned it
✅ Created a branch
✅ Edited a file
✅ Opened a PR
✅ Passed auto-validation
✅ Made your first open-source contribution!

---

## ❓ FAQ

### Why Only `README.md`?

This is a **safe sandbox** for beginners to practice open-source without fear of breaking anything. The bot only accepts PRs that update `README.md` (specifically the contributors section).

### What Happens If I Break a Rule?

Your PR will:

* Be flagged automatically
* Show an ❌ message
* Not be merged until corrected

You can simply fix it and push again to the same branch.

---

## 📚 More Resources

* [Chai aur Git Docs](https://docs.chaicode.com/youtube/chai-aur-git/introduction/)
* [GitHub Docs](https://docs.github.com/en)
* [First Contributions](https://firstcontributions.github.io/)

---

## 💬 Need Help?

Open an [Issue](https://github.com/gauravslnk/git-learners-lab/issues) or reach out via our community group.

---

## ❤️ Thank You!

We’re glad you’re here. This project is your first step into the world of open source — and we’re cheering you on 🚀
