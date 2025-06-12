# 🌱 Step-by-Step GitHub Contribution Guide

> A complete **beginner-friendly guide** to help you contribute to this project easily — even if it's your **first time using GitHub**.

---

## ✅ Prerequisites (Only Once)

### 1️⃣ Install Git

Download and install Git from [https://git-scm.com/downloads](https://git-scm.com/downloads)

After installing, check it by running:

```bash
git --version
```

✅ You should see something like: `git version 2.xx.x`

---

## 🔁 Step 1: Fork This Repository

1. Go to the main repository:
   👉 [https://github.com/gauravslnk/git-learners-lab](https://github.com/gauravslnk/git-learners-lab)
2. Click the **Fork** button (top-right)
3. Select your GitHub account

This creates your own **copy** of the repository.

---

## 💻 Step 2: Clone Your Fork Locally

1. Open your forked repo
2. Click the green `<> Code` button and copy the HTTPS link
3. In terminal or Git Bash, run:

```bash
git clone https://github.com/your-username/git-learners-lab.git
cd git-learners-lab
```

---

## 🌿 Step 3: Create a New Branch

```bash
git checkout -b add-my-profile
```

✅ This creates a separate branch so your changes stay organized.

---

## 📝 Step 4: Add Yourself to the Contributors Table

### Open the project in VS Code:

```bash
code .
```

1. Open the `README.md` file
2. Scroll to the **Contributors** table (inside `<!-- ALL-CONTRIBUTORS-LIST:START -->`)
3. Add your block like this at the **end** of the last row:

```html
<td align="center">
  <a href="https://github.com/your-username">
    <img src="https://avatars.githubusercontent.com/your-id" width="100px;" alt="Your Name" />
    <br />
    <sub><b>Your Name</b></sub>
  </a>
</td>
```

### 🔁 Replace:

| What            | Replace with                                                               |
| --------------- | -------------------------------------------------------------------------- |
| `your-username` | Your GitHub username                                                       |
| `your-id`       | Right-click your GitHub profile pic → Copy image address (grab the number) |
| `Your Name`     | Your actual name                                                           |

✅ Make sure it’s **only 1 contributor** and **added at the end**

---

## 📌 Step 5: Save & Commit Your Changes

```bash
git add README.md
git commit -m "Added My Name to Contributors List"
```

---

## 🚀 Step 6: Push Your Changes

```bash
git push origin add-my-profile
```

---

## 🔃 Step 7: Create a Pull Request (PR)

1. Go to your GitHub fork
2. You’ll see a button: `Compare & pull request` — click it
3. Add a title like:

```
Added My Name to Contributors List ✨
```

4. Click `Create Pull Request`

---

## 🤖 Step 8: Let the Bot Validate Your PR

Wait a few seconds. The **bot will validate** your submission automatically.

### ✅ If successful:

* Green checkmark appears on the PR
* Bot comments: `✅ Validation passed! Thanks for contributing 💫`

### ❌ If failed:

* Red ❌ and a bot comment tells you what’s wrong (e.g., duplicate, wrong order)

You can fix the issue and push again — no need to create a new PR.

---

## 🎉 Step 9: Celebrate!

You’ve just:

* ✅ Forked a repo
* ✅ Cloned it
* ✅ Created a branch
* ✅ Edited a file
* ✅ Made a Pull Request
* ✅ Passed automated validation
* ✅ Contributed to open source!

---

