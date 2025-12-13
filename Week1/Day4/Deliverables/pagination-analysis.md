# Pagination Analysis (GitHub API)

## What is this task about?
In this task, I learned how GitHub sends large amounts of data in **pages** instead of sending everything at once.  
This process is called **pagination**.

When a user has many repositories, GitHub does not return all repositories in one response.  
Instead, it sends them **page by page**.

---

## What is Pagination? 
Pagination means:
- Big data is broken into **small parts**
- Each part is called a **page**
- We request one page at a time

Example:
- Page 1 → first 5 repos
- Page 2 → next 5 repos
- Page 3 → next 5 repos (may be empty)

---

## API Endpoint Used
https://api.github.com/users/octocat/repos


---

## Query Parameters Used

### `page`
- Tells GitHub **which page** we want
- Example:
  - `page=1` → first page
  - `page=2` → second page

### `per_page`
- Tells GitHub **how many items per page**
- I used:
per_page=5

This means:
- Maximum 5 repositories per page

---

## Commands I Used

### Page 1
curl -s -D repos-page1-headers.txt
"https://api.github.com/users/octocat/repos?page=1&per_page=5
"
-o repos-page1.json


### Page 2
curl -s -D repos-page2-headers.txt
"https://api.github.com/users/octocat/repos?page=2&per_page=5
"
-o repos-page2.json


### Page 3
curl -s -D repos-page3-headers.txt
"https://api.github.com/users/octocat/repos?page=3&per_page=5
"
-o repos-page3.json


---

## Files Generated

| File Name | Purpose |
|---------|--------|
| repos-page1.json | Repository data for page 1 |
| repos-page2.json | Repository data for page 2 |
| repos-page3.json | Repository data for page 3 |
| repos-page1-headers.txt | Headers for page 1 |
| repos-page2-headers.txt | Headers for page 2 |
| repos-page3-headers.txt | Headers for page 3 |

---

## What I Observed

### Page 1
- Returned repository data
- Contained up to **5 repositories**
- Headers included a **Link** header

### Page 2
- Returned repository data
- Also had up to **5 repositories**
- Headers showed pagination links

### Page 3
- Returned an **empty array (`[]`)**
- This means **no more repositories exist**
- This is a valid and expected response

---

## Understanding the `Link` Header

Example:
Link: https://api.github.com/...page=2
; rel="next",
https://api.github.com/...page=34
; rel="last"


### Meaning:
- `rel="next"` → URL of the next page
- `rel="last"` → URL of the last page

This tells us:
- More data exists
- Where to fetch it from

---

## Why Pagination is Important
- Saves bandwidth
- Improves performance
- Prevents large responses
- Makes APIs faster and safer

---

## Conclusion
- GitHub API uses pagination to manage large datasets
- I successfully fetched multiple pages using `page` and `per_page`
- I verified pagination using the `Link` response header
- Empty response on page 3 confirmed the end of data

This task helped me understand how real-world APIs handle large amounts of data efficiently.
