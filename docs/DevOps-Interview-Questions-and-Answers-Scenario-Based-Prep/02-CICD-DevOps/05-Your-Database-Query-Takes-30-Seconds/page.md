# List access keys for a user
aws iam list-access-keys --user-name YOUR_USER

# Deactivate a key (optional, before deleting)
aws iam update-access-key --user-name YOUR_USER --access-key-id AKIAEXAMPLE --status Inactive

# Delete the compromised key
aws iam delete-access-key --user-name YOUR_USER --access-key-id AKIAEXAMPLE

# Create a new key (outputs JSON with the new credentials)
aws iam create-access-key --user-name YOUR_USER
```

Why rotate first? If the secret remains valid while you rewrite history, attackers can continue to use it even after you remove it from commits.

***

### Step 2 — Purge the secret from Git history (rewrite history)

After credentials are rotated and invalidated, rewrite repository history to remove the secret from all commits. The two commonly used tools:

* `git-filter-repo` (recommended, actively maintained)
* BFG Repo-Cleaner (simpler for straightforward file deletions)

Important: Both approaches require a mirrored clone and will change commit SHAs. After forced-pushing the cleaned history, everyone with clones must re-clone or reset; forks and mirrors may still contain the secret.

Example: remove a file from all commits with `git-filter-repo`:

```shell theme={null}
# Clone a bare mirror
git clone --mirror git@github.com:your/repo.git
cd repo.git

# Remove a specific file from all commits
git filter-repo --invert-paths --paths path/to/secret.file

# Expire reflog, run GC, and force-push cleaned history
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

Example: redact specific secret strings with `git-filter-repo`:

```shell theme={null}
# Create a replace-text file (format: "literal==>replacement" or just "literal")
# secrets-to-redact.txt content example:
git clone --mirror git@github.com:your/repo.git
cd repo.git

# Replace / redact strings listed in secrets-to-redact.txt
git filter-repo --replace-text ../secrets-to-redact.txt

git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

Example: remove files using BFG (good for deleting private keys, etc.):

```shell theme={null}
# Mirror clone
git clone --mirror git@github.com:your/repo.git
java -jar bfg.jar --delete-files id_rsa repo.git

cd repo.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

Operational notes:

* Coordinate with your team before force-pushing rewritten history.
* Ask collaborators to re-clone or reset their local repositories to avoid reintroducing old commits.
* If the repository was forked or mirrored externally, those copies may still contain the secret — contact maintainers or owners of forks if possible.

<Callout icon="warning">
  Rewriting history and force-pushing affects every collaborator and all clones. Coordinate and require everyone to re-clone or perform a clean reset. Never force-push to shared branches without communication.
</Callout>

***

### Step 3 — Prevent future leaks (scan before commit)

Add automated checks to catch secrets before they are committed and pushed. Implement pre-commit hooks and CI scanning.

Popular tools:

* detect-secrets — heuristic-based secret scanner (Yelp)
* gitleaks — fast, configurable detection tool
* pre-commit — hook framework to run detection tools locally

Example `.pre-commit-config.yaml` using `detect-secrets` and `gitleaks`:

```yaml theme={null}
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.3.0
    hooks:
      - id: detect-secrets-hook
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/zricethezav/gitleaks
    rev: v8.2.0
    hooks:
      - id: gitleaks
        args: ['--verbose']
```

Install and enable pre-commit locally:

```shell theme={null}
pip install pre-commit
pre-commit install
pre-commit run --all-files  # test it now
```

<Callout icon="lightbulb">
  Short checklist when you discover leaked secrets:

  1. Rotate/revoke the secrets immediately.
  2. Rewrite Git history to remove secrets.
  3. Force-push the cleaned history and coordinate with your team.
  4. Add pre-commit hooks and CI scanning to prevent recurrence.
</Callout>

***

## Tools and quick references

| Tool / Resource   |                                                  Purpose | Example / Link                                                                           |
| ----------------- | -------------------------------------------------------: | ---------------------------------------------------------------------------------------- |
| `git-filter-repo` | Recommended for history rewriting and string replacement | [https://github.com/newren/git-filter-repo](https://github.com/newren/git-filter-repo)   |
| BFG Repo-Cleaner  |                       Easy removal of files from history | [https://github.com/rtyley/bfg-repo-cleaner](https://github.com/rtyley/bfg-repo-cleaner) |
| detect-secrets    |                       Secret detection for pre-commit/CI | [https://github.com/Yelp/detect-secrets](https://github.com/Yelp/detect-secrets)         |
| gitleaks          |                 Fast secrets detection with many presets | [https://github.com/zricethezav/gitleaks](https://github.com/zricethezav/gitleaks)       |
| pre-commit        |             Framework to run hooks locally before commit | [https://pre-commit.com/](https://pre-commit.com/)                                       |

***

## Final notes / best practices

* Rotating credentials immediately is the top priority. Cleaning Git history is important but secondary—do it after rotation.
* Automate secret detection in local development and CI to stop leaks before they reach remote repositories.
* Treat any secret exposed in a public repository as compromised: assume it was collected and acted upon.
* Maintain an incident playbook that includes credential rotation, history cleaning, and team communication steps.

### Links and references

* [git-filter-repo](https://github.com/newren/git-filter-repo)
* [BFG Repo-Cleaner](https://github.com/rtyley/bfg-repo-cleaner)
* [detect-secrets (Yelp)](https://github.com/Yelp/detect-secrets)
* [gitleaks](https://github.com/zricethezav/gitleaks)
* [pre-commit](https://pre-commit.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/370000ef-b6bc-4986-8d29-0793ebb2c9e7/lesson/2b7b52a8-7642-4da9-a619-021b47120033" />
</CardGroup>


# Your Database Query Takes 30 Seconds

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/CICD-DevOps/Your-Database-Query-Takes-30-Seconds/page

Explains diagnosing and fixing slow SQL queries by examining execution plans, adding appropriate indexes, eliminating N+1 application patterns, optimizing joins and statistics before considering hardware upgrades.

In this lesson we walk through a common DevOps / backend interview scenario:

A developer writes a query that joins four tables. It takes thirty seconds to return results. The proposed fix? Upgrade the database to a bigger instance.

Is that the right move? Almost never. A slow query is typically a code, schema, or plan problem — not a RAM or CPU problem. Upgrading from 8 GB to 32 GB might reduce the time from thirty seconds to twenty‑five seconds, but you still have a fundamentally broken query and ongoing cost.

Before making any changes, inspect the query plan and the application behavior: that’s where the real cause usually reveals itself.

<Frame>
  <img alt="The image illustrates a conceptual problem-solving approach, highlighting that issues are almost never hardware-related, and often stem from code problems. It suggests that upgrading from 8GB to 32GB might be a common, but potentially misguided, solution." />
</Frame>

## Common root causes

Most slow queries fall into a few predictable categories:

* Missing or wrong indexes
* Application-layer N+1 query patterns
* Inefficient joins and `SELECT *` usage
* Outdated statistics, bad planner estimates, or inappropriate join orders

## Missing indexes

This is the number-one culprit. Without an index, a database may scan millions of rows instead of reading a handful — like flipping through every page of a phone book instead of using the alphabetical tabs. A single well-placed index can turn 30 seconds into tens of milliseconds.

<Frame>
  <img alt="The image displays text about a costly query issue, emphasizing that the query is still problematic, and highlights &#x22;missing indexes&#x22; as a usual suspect." />
</Frame>

## The N+1 problem

This is an application-layer issue. Example pattern:

* Your code fetches 100 users.
* Then it runs a separate query for each user's orders.
* Result: 101 round trips (1 + 100) when a single join or a batched query could return everything in one round trip.

N+1 often does not show up in a standalone SQL review because the extra queries are generated in application loops or from lazy-loaded relationships.

## Bad joins and SELECT \*

A multi-table join isn’t inherently slow. The problem arises when:

* You join on non-indexed columns, causing full scans.
* You fetch every column with `SELECT *` when you only need a few fields (wasted I/O and CPU).
* The planner chooses an expensive join order or hash join because statistics are stale.

Best practice: select only the columns you need and join on indexed keys.

## What to do (practical checklist)

<Callout icon="lightbulb">
  Always run the query planner/executor to see what the database is actually doing before making changes.
</Callout>

## Step 1 — Run EXPLAIN / EXPLAIN ANALYZE

This is non-negotiable. Use the RDBMS’s explain facility to see the chosen plan and actual runtime stats.

* PostgreSQL: `EXPLAIN ANALYZE <query>;` (add `BUFFERS` for I/O stats)
* MySQL: `EXPLAIN FORMAT=JSON <query>;` and consider `ANALYZE TABLE` to refresh stats
* SQL Server: Use the Actual Execution Plan

Look for: full table scans, large row estimates, ignored indexes, expensive sorts, or repeated nested loops.

Example (PostgreSQL):

```sql theme={null}
EXPLAIN ANALYZE
SELECT o.id, o.total, u.name
FROM orders o
JOIN users u ON u.id = o.user_id
WHERE o.created_at >= '2026-01-01';
```

## Step 2 — Add the right indexes

* Index columns used in `WHERE`, `JOIN`, `GROUP BY`, and `ORDER BY`.
* Use composite indexes for multi-column filters. Create them in the column order the query uses (leading-column matters).
* Avoid indexing every column — unnecessary indexes increase write cost and storage.
* Consider covering indexes if the index can satisfy the entire query without touching the table.

## Step 3 — Fix the application layer

* Replace lazy-loaded per-row queries with eager loading or explicit joins.
* Batch requests (e.g., `WHERE id IN (...)`) instead of issuing one query per item.
* Implement pagination or streaming for large result sets rather than reading everything into memory.

## When to consider additional hardware

Only after you’ve exhausted query, schema, and configuration fixes should you consider scaling or specialized systems.

* Use read replicas to offload reporting/read-heavy workloads — they protect the primary but don’t fix a bad query.
* For heavy analytics over very large datasets, consider OLAP systems (e.g., Redshift, BigQuery, ClickHouse).
* Tune database configuration (work\_mem, shared\_buffers, effective\_cache\_size, etc.) and ensure statistics are current (`ANALYZE` / autovacuum working).

<Callout icon="warning">
  Do not use larger instances to hide slow queries. Upgrading hardware without addressing the root cause is expensive and temporary.
</Callout>

## Quick reference table

|                  Problem | What to check                                      | Quick fix                                    |
| -----------------------: | -------------------------------------------------- | -------------------------------------------- |
|    Too many rows scanned | EXPLAIN ANALYZE → sequential scans on large tables | Add or adjust indexes                        |
|              N+1 queries | Application logs / query tracing (APM)             | Eager load, batch queries, JOINs             |
|    Large result payloads | Query selects `*` or many columns                  | Select only required columns; use pagination |
| Planner chooses bad plan | Stale statistics, wrong estimates                  | `ANALYZE`, update stats, check histograms    |
|     Read-heavy reporting | Primary instance CPU/IO spikes                     | Offload to read replicas or a data warehouse |

## Summary

The pattern is consistent: diagnose first, then fix the root cause. Use the planner and application traces to find whether the issue is an index, an application loop, a bad join, or stale statistics. Throwing hardware at a bad query is like putting a bigger engine on a car with a clogged fuel line — it wastes money and delays the inevitable fix.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/370000ef-b6bc-4986-8d29-0793ebb2c9e7/lesson/d9fd417e-1cee-4832-b412-a513ef2b44ca" />
</CardGroup>
