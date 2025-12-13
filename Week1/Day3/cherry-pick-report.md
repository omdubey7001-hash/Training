# Cherry-Pick Report

## Branch Used
`release/v0.1`

This branch was created from commit:

ae639d8 – Add line 4

---

## Purpose
The goal was to create a stable `release/v0.1` branch by:

1. Avoiding the buggy commit (`Add buggy line 5`)
2. Cherry-picking only the clean commits from `master`
3. Ensuring `app.js` contains all good features without the bug

---

## Buggy Commit Identified by Git Bisect

Using `git bisect`, the first bad commit was found:

f10fefa – Add buggy line 5

This commit introduced:

consol.log("Line 5: THIS LINE HAS A BUG!");

This commit was **not** cherry-picked.

---

## Cherry-Picked Commits

The following commits from `master` were cherry-picked into `release/v0.1`:

2e4e632 – Add line 6  
8db29c6 – Add line 7  
feaeda1 – Add line 8  
67ab736 – Add line 9  
a1464b0 – Add line 10

Commands used:

git cherry-pick 710180e  
git cherry-pick 77d3037  
git cherry-pick f1edec8  
git cherry-pick bd11122  
git cherry-pick 57bce33

---

## Conflict Encountered

During cherry-pick of `710180e (Add line 6)` a conflict occurred due to the buggy line 5.

Git showed:

<<<<< HEAD  
console.log("Line 4: Preparing environment");  
=====  
consol.log("Line 5: THIS LINE HAS A BUG!");  
console.log("Line 6: Initialization complete");  
>>>>> 710180e

### Conflict Resolution

Resolved by removing buggy line 5 and keeping line 6:

console.log("Line 6: Initialization complete");

Then:

git add app.js  
git cherry-pick --continue

---

## Final app.js in release branch

console.log("Line 1: Application starting...");  
console.log("Line 2: Loading modules...");  
console.log("Line 3: Establishing database connection");  
console.log("Line 4: Preparing environment");  
console.log("Line 6: Initialization complete");  
console.log("Line 7: Starting server");  
console.log("Line 8: Server running at port 3000");  
console.log("Line 9: Monitoring health checks");  
console.log("Line 10: App fully running");

---

## Summary

- Buggy commit was excluded  
- Clean commits (6–10) were cherry-picked  
- One conflict occurred and was fixed  
- `release/v0.1` is now stable

# End of Report
