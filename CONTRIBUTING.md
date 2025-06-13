# 🌱 Welcome to Git Learners Lab – Contributor Guide

> A beginner-friendly, step-by-step guide to help you make your **first open-source contribution** – even if you’ve never used Git before!

---

## ✅ Prerequisites (One-time Setup)

Before contributing, please ensure:

* 🔧 [Git is installed](https://git-scm.com/downloads)
* 🧑‍💻 You have a GitHub account
* 💡 (Optional) [VS Code installed](https://code.visualstudio.com/) as your editor

Check Git installation:

```bash
git --version
```

You should see something like `git version 2.xx.x`.

---

## 📜 Contribution Rules & Guidelines

We’ve made the contribution process super simple! Here's what you need to know:

### ✅ Do:

* Create **only one `.txt` file per contributor**
* Add your file to the **`contributors/`** folder
* Name the file the same as your **GitHub username** (e.g., `yourusername.txt`)
* Follow the fun format inside the file (see below)
* You're allowed to update your file later with new PRs too

### ❌ Don't:

* Modify any files outside the `contributors/` folder
* Add multiple `.txt` files in one PR
* Change other people's files
* Add `.md`, `.js`, `.html`, etc. — only `.txt` allowed

> ⚠️ PRs that break these rules will not be merged.

---

## 📝 Your `.txt` File Format

Each `.txt` file should follow this simple format:

```
Your Full Name
Your Favorite Celebrity or Public Figure
```

---

## 📅 Step-by-Step Guide to Contribute

---

### 🔀 1. Fork This Repository

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

### ✨ 4. Create Your Contributor `.txt` File

1. Open the project in VS Code (or any editor)
2. Go to the `contributors/` folder
3. Create a new file named: `your-github-username.txt`
4. Inside that file, add:

```
Your Full Name
Your Favorite Celebrity or Public Figure
```

Example:

```
John Doe
Jane Doe
```

---

### 📂 5. Save, Add, and Commit Your Changes

```bash
git add contributors/your-github-username.txt
git commit -m "Added <Your Name> as a contributor"
```

---

### 🚀 6. Push Your Branch

```bash
git push origin add-your-username
```

---

### 🔄 7. Create a Pull Request (PR)

1. Go to your fork on GitHub
2. Click **Compare & pull request**
3. Use a clear title like:

```text
Added My Name as Contributor ✨
```

4. Click **Create pull request**

---

### 🤖 8. Let the Bot Validate Your PR

Our GitHub bot will check your PR:

#### ✅ If everything is good:

* Your PR will be **automatically merged** 🎉
* You’ll see a success message

#### ❌ If something’s wrong:

* The bot will reject the PR
* Just fix your file and push again — no need to reopen

---

### 🎉 9. Celebrate!

You just:
✅ Forked a repo
✅ Cloned it
✅ Created a branch
✅ Added a file
✅ Opened a PR
✅ Passed auto-validation
✅ Made your first open-source contribution!

---

## ❓ FAQ

### Why Only `.txt` Files in `contributors/`?

This keeps the project beginner-safe. You can experiment without worrying about breaking anything important.

### Can I Update My File Later?

Yes! Create a new branch, update your `.txt` file, and make another PR.

---

## 📚 More Learning Resources

* [Chai aur Git Docs](https://docs.chaicode.com/youtube/chai-aur-git/introduction/)
* [GitHub Docs](https://docs.github.com/en)
* [First Contributions](https://firstcontributions.github.io/)

---

## ❤️ Thank You!

We’re thrilled to have you here. This is your first step into open source — and we’re here to cheer you on 🚀
