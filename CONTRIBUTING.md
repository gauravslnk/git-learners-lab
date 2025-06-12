# ✨ Contributor Guide

Welcome to **git-learners-lab** – your first step into the world of GitHub and Open Source!

Follow this guide to add yourself to the contributors list and make your very first Pull Request 🚀

---

## 🛠️ Prerequisites

- Install Git: [Download Git](https://git-scm.com/downloads)
- Create a GitHub account (if you don’t have one)

---
---

## ✅ Contribution Rules

- Submit only **one** new contributor per PR.
- Ensure your name is added to the **end of the table**.
- Avoid **duplicate entries**.
- Each row must have **no more than 7 contributor cards**.
- Only modify the `README.md` file unless you're fixing something else.

Your PR will be automatically validated and commented on. ❗

---
> 💡 Tip: Use `Ctrl + Shift + V` in VS Code to preview how the README looks before committing.

---

## 📝 Steps to Add Yourself as a Contributor

### 1. Fork this Repository

Head over to the main repo: [git-learners-lab](https://github.com/gauravslnk/git-learners-lab)  
Click the **`Fork`** button at the top-right corner.

Then click **`Create fork`**.

---

### 2. Clone Your Fork

Click the green **`<> Code`** button on your forked repo and copy the URL.

Open your terminal and run:

```bash
git clone https://github.com/<your-username>/git-learners-lab.git
cd git-learners-lab
````

---

### 3. Create a New Branch

Creating a branch keeps your changes separate:

```bash
git checkout -b add-your-name
```

---

### 4. Add Your Profile Card in `README.md`

Open the `README.md` file using VS Code or any editor.

Append this snippet at the end of the contributor section:

```html
<td align="center">
  <a href="https://github.com/your-username">
    <img src="https://avatars.githubusercontent.com/your-id" width="100px;" alt="Your Name"/>
    <br />
    <sub><b>Your Name</b></sub>
  </a>
</td>
```

✅ Replace:

* `href` → your GitHub profile URL
* `src` → your profile picture URL *(right-click → “Copy image address”)*
* `Your Name` → your actual name

---

### 5. Save and Commit Your Changes

```bash
git add README.md
git commit -m "Added <Your Name> to contributors list"
```

---

### 6. Push Your Changes to GitHub

```bash
git push origin add-your-name
```

---

### 7. Create a Pull Request (PR)

1. Go to your forked repo on GitHub.
2. Click **`Compare & pull request`**
3. Write a message like:
   *"Added my name to the contributors list ✨"*
4. Click **`Create pull request`**

---

### 8. 🎉 Celebrate!

You just submitted your first PR!
Wait for a maintainer to review and merge it.

---

## 📚 Learn More

Want to dig deeper into Git and GitHub?
Check out this excellent beginner blog:
➡️ [Chai aur Git - Docs](https://docs.chaicode.com/youtube/chai-aur-git/introduction/)

---

## ❤️ Thank You

Thank you for being part of this journey. We’re excited to welcome you to the world of Open Source!

---

> For any issues, feel free to reach out by opening an issue or asking in our DSC group.

