Pagination Analysis — GitHub API (octocat/repos)

This document analyzes the pagination behavior of the GitHub REST API when fetching repositories for the user octocat using the endpoint:

https://api.github.com/users/octocat/repos


We performed requests for page 1, page 2, and page 3, each with per_page=5, and inspected the HTTP Link headers returned by the server.

1. Request URLs Used
Page	URL
Page 1	https://api.github.com/users/octocat/repos?page=1&per_page=5
Page 2	https://api.github.com/users/octocat/repos?page=2&per_page=5
Page 3	https://api.github.com/users/octocat/repos?page=3&per_page=5

Each page was fetched using:

curl -s -D repos-pageX-headers.txt "URL" -o repos-pageX.json

2. Observed Link Headers

The GitHub API uses the Link header to provide navigation URLs to other pages.
After running grep -i '^link:' repos-pageX-headers.txt, we observed:

Page 1 — Link Header

Example:

Link: <https://api.github.com/user/000/repos?page=2>; rel="next",
      <https://api.github.com/user/000/repos?page=34>; rel="last"


Meaning:

There is a next page → page=2

The last page is 34

Page 2 — Link Header

Example:

Link: <https://api.github.com/user/000/repos?page=1>; rel="prev",
      <https://api.github.com/user/000/repos?page=3>; rel="next",
      <https://api.github.com/user/000/repos?page=34>; rel="last",
      <https://api.github.com/user/000/repos?page=1>; rel="first"


Meaning:

There is a previous page (1)

There is a next page (3)

First page = 1

Last page = 34

Page 3 — Link Header

Example:

Link: <https://api.github.com/user/000/repos?page=2>; rel="prev",
      <https://api.github.com/user/000/repos?page=4>; rel="next",
      <https://api.github.com/user/000/repos?page=34>; rel="last",
      <https://api.github.com/user/000/repos?page=1>; rel="first"


Meaning:

Previous page = 2

Next page = 4

First page = 1

Last page = 34

If GitHub had returned a last-page response, only prev and first would appear.

3. Understanding Pagination Links

The GitHub pagination system uses:

rel=""	Meaning
next	URL of the next page
prev	URL of the previous page
first	URL of the first page
last	URL of the last page

The API never tells you the total number of items directly, but you can determine:

Whether more pages exist

What page you're currently on

How to navigate to other pages

Links appear only when needed:

Page 1 → Has next, last

Middle pages → Have all (prev, next, first, last)

Last page → Only prev, first

4. How to Navigate Pages Programmatically

Given a Link header:

Link: <URL1>; rel="next", <URL2>; rel="last"


You:

Parse the header by commas ,

Split each segment by ;

Extract the URL inside < >

Use the URL where rel="next" to fetch the next page

Stop when rel="next" is absent

5. Conclusion

GitHub provides pagination through the Link header following RFC 5988.

Using page + per_page params and the Link header, you can access any page of results.

The last relation helps determine how many pages exist.

During this task, pages 1 → 3 behaved exactly according to GitHub’s standard pagination pattern.
