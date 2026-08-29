# Searching and Filtering Issues

Source: https://notes.kodekloud.com/docs/GitHub-Foundations-Certification/Issues/Searching-and-Filtering-Issues/page

Guide to using GitHub search qualifiers and queries to filter and find issues and pull requests efficiently, with examples and tips for personal and team workflows.

How can we search and filter issues and pull requests on GitHub?

[GitHub's search bar](https://docs.github.com/en/issues/searching-for-issues-and-pull-requests/searching-issues-and-pull-requests) is a powerful filtering engine. While the UI provides handy dropdowns for authors, labels, and states, typing queries directly into the search box unlocks far more precise results. This guide explains the most useful qualifiers, shows examples you can copy, and gives quick tips for personal and team workflows.

## Why type queries instead of using the UI?

Typing queries lets you:

* Combine multiple qualifiers for very focused results.
* Search specific fields (title, body, comments).
* Exclude items with the NOT operator.
* Save time with reusable queries for your workflow or team dashboards.

## Common qualifiers and how to use them

| Qualifier                              | Purpose                                  | Example                         |
| -------------------------------------- | ---------------------------------------- | ------------------------------- |
| `is:issue` / `is:pr`                   | Limit results to issues or pull requests | `is:issue is:open`              |
| `is:open` / `is:closed`                | Filter by open or closed state           | `is:pr is:closed`               |
| `assignee:@me`                         | Items assigned to the signed-in user     | `is:open is:issue assignee:@me` |
| `author:<username>`                    | Items created by a specific user         | `author:contoso is:pr`          |
| `label:<name>`                         | Filter by label                          | `label:bug is:open`             |
| `in:comments` / `in:title` / `in:body` | Restrict text search to a specific field | `is:pr in:comments sidebar`     |
| `linked:pr` / `-linked:pr`             | Items with or without linked PRs         | `label:bug -linked:pr`          |
| `-` (minus sign)                       | NOT operator to exclude results          | `label:bug -linked:pr`          |

## Quick, copy-ready search queries

```text theme={null}
