# 🍒 Cherry-Pick Report  
**Repository Task — Day 3**

---

## 📌 Task Goal
The goal of this task was to **selectively transfer verified commits** from one branch to another **without merging unwanted history**, ensuring a **stable and clean release branch**.

This was achieved using **Git Cherry-Pick**.

---

## 🧠 Concept in Simple Words
> Cherry-pick means:  
> **“Take only what is good, leave everything else.”**

Instead of merging a full branch (which may contain bugs or experiments), only **specific, trusted commits** are applied to the target branch.

---

## 🧩 Initial Situation
- Multiple commits existed across branches
- One commit introduced a **buggy line**
- The release branch had to remain **production-safe**

Merging directly was **not an option**.

---

## 🛠️ Actions Performed (Step-by-Step)

### ✅ Step 1: Analyze Commit History
- Reviewed commit logs
- Identified **stable commits**
- Marked the **buggy commit to skip**

📌 This step ensured informed decision-making before applying changes.

---

### ✅ Step 2: Switch to Target Branch
- Moved to `release/v0.1`
- Prepared it to receive selected changes

This branch represents the **final deliverable**, so stability was mandatory.

---

### ✅ Step 3: Cherry-Pick Selected Commits
- Applied commits **one at a time**
- Maintained correct logical order
- Avoided applying the buggy commit

This ensured **only clean functionality** was transferred.

---

### ⚠️ Step 4: Conflict Resolution
A conflict occurred in `app.js` during cherry-pick.

**Resolution strategy:**
- Inspected conflicting sections
- Removed the buggy statement
- Preserved valid `console.log()` lines
- Completed cherry-pick successfully

📌 Conflict resolution proved understanding of both code and Git flow.

---

### 🔍 Step 5: Verification via Commit Graph
The commit graph was inspected to confirm:

- ✔ Correct commit sequence
- ✔ Buggy commit excluded
- ✔ No unwanted merge history
- ✔ Clean linear release timeline

---

## 📊 Why Commit Graph Was Important
The graph visually confirmed that:
- Cherry-pick was used instead of merge
- Branch histories remained independent
- Only intentional changes existed in `release/v0.1`

This validates **professional Git usage**.

---

## 🎯 Final Outcome
The `release/v0.1` branch now:
- Contains **only verified commits**
- Excludes experimental or buggy changes
- Maintains a **clean and readable history**
- Is safe for release or deployment

---

## 🧾 Key Learnings
- Cherry-pick gives **precise control** over commits
- Commit graphs help validate branch integrity
- Conflict resolution is part of real-world Git usage
- Clean history = professional workflow

---

## 🏁 Conclusion
This task demonstrates practical understanding of **Git Cherry-Pick**, conflict handling, and commit history verification — ensuring only stable and intentional code reaches the release branch.
