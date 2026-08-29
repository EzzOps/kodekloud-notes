# Amazon DevOps Parse This Nginx Log

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/CICD-DevOps/Amazon-DevOps-Parse-This-Nginx-Log/page

Explains using awk to parse NGINX access logs, correctly identify status and URL fields to count 5xx errors, and avoid false matches from naive pattern searches.

So what question do companies like Amazon actually ask in their DevOps interviews? They rarely ask textbook definitions — they give practical problems.

In this lesson we will work through one such problem: given an [NGINX](https://nginx.org/en/docs/) access log like this:

```text theme={null}
/var/log/nginx/access.log
127.0.0.1   - - [08/Apr/06:25:16 +0000] "GET /api/event HTTP/2.0" 200 937
192.168.1.5 - - [08/Apr/06:25:42 +0000] "POST /api/checkout HTTP/2.0" 503 0
10.0.0.42   - - [08/Apr/06:25:58 +0000] "GET /api/orders HTTP/2.0" 500 124
8.8.8.8     - - [08/Apr/06:26:11 +0000] "DELETE /api/cart/77 HTTP/2.0" 200 84
172.16.0.5  - - [08/Apr/06:26:37 +0000] "GET /api/checkout HTTP/2.0" 502 89
```

Which URLs are throwing the most server errors (5xx)?

A common one-liner people try uses [awk](https://www.gnu.org/software/gawk/), sort, uniq, and head. The idea: extract the status code to filter 5xx, then print the URL, count and sort.

[Awk](https://www.gnu.org/software/gawk/) reads the log line-by-line, splits it into fields by whitespace, and lets you pick fields like `$1`, `$2`, etc. From each line we need two pieces:

* the status code (to select 5xx responses), and
* the URL (to count how many errors each URL produces).

If we label the fields naively (assuming whitespace-separated fields):

* \$1 = IP
* $2, $3 = the two dashes
* \$4 = timestamp (but note: it contains spaces and brackets)
* \$5 = request (but it contains method, URL, and protocol separated by spaces)
* \$6 = status
* \$7 = response size

This naive labeling leads to a command like this:

```bash theme={null}
$ awk '$6 ~ /^5/{print $5}' access.log | sort | uniq -c | sort -rn | head -10
```

When you run this, you might get no output or incorrect counts. Why? Because [awk](https://www.gnu.org/software/gawk/) splits on whitespace: the timestamp contains spaces and the request field uses spaces between method, URL, and protocol. So awk doesn't see the timestamp or the quoted request as single fields.

Consider this example log line:

```text theme={null}
192.168.1.5 - - [08/Apr:06:25:42 +0000] "POST /api/checkout HTTP/2.0" 503 0
```

With awk's default splitting:

* the timestamp becomes two fields (e.g., fields 4 and 5),
* the quoted request becomes three fields (e.g., fields 6, 7, and 8).

Therefore our original labels are wrong. After accounting for the splitting, the correct field mapping is:

* \$1 = IP
* $2, $3 = the two dashes
* $4 and $5 = timestamp (split into two fields)
* \$6 = method (e.g., `"POST`)
* \$7 = URL (e.g., /api/checkout)
* \$8 = protocol (e.g., HTTP/2.0")
* \$9 = status code
* \$10 = response size

So the working command uses `$9` for status and `$7` for the URL:

```bash theme={null}
$ awk '$9 ~ /^5/ {print $7}' access.log | sort | uniq -c | sort -rn | head -10
```

This correctly selects lines where the status code is in the 5xx family and prints the requested URL for counting.

Callout: When parsing logs with awk, always inspect how fields are split — quoted strings and bracketed timestamps commonly break naive field indexing.

<Callout icon="lightbulb">
  [Awk](https://www.gnu.org/software/gawk/) splits on whitespace by default. Quoted sections like the request (`"METHOD URL PROTOCOL"`) will be split into multiple fields unless you adjust the field separator or account for the split in your indices.
</Callout>

A common follow-up interview question is: what's wrong with matching the literal string `500` anywhere on the line?

For example:

```bash theme={null}
$ awk '/500/' access.log
```

This matches any line containing the substring `500` anywhere — in the status code, in the URL, or in the response size. That produces false positives. For instance, consider these lines:

```text theme={null}
10.0.0.42   - - [08/Apr:06:25:18 +0000] "GET /api/event HTTP/2.0" 500 124
8.8.8.8     - - [08/Apr:06:25:34 +0000] "GET /v500/items HTTP/2.0" 200 500
4.4.4.4     - - [08/Apr:06:25:51 +0000] "GET /p/500-error-fix HTTP/2.0" 200 812
5.5.5.5     - - [08/Apr:06:25:00 +0500] "GET /api/login HTTP/2.0" 200 84
```

The second line contains `500` in the URL and the response size; the third line contains `500` in the URL path. Using `/500/` as a pattern will match those lines even though their status codes are not 500.

The correct approach is to anchor your match to the status code field. Using field matching avoids accidental matches in other parts of the line:

* Exact match for 500:

```bash theme={null}
$ awk '$9 == 500 {print $7}' access.log
```

* Match the entire 5xx family:

```bash theme={null}
$ awk '$9 ~ /^5/ {print $7}' access.log
```

Summary — what interviewers are checking:

* Do you understand awk fields and how whitespace splitting affects field indices?
* Do you properly anchor your regex or use field equality when matching status codes?
* Can you distinguish between searching the whole line vs matching a specific field?

If you want a more robust parser for complex logs, consider using tools that respect quoted fields (e.g., [awk](https://www.gnu.org/software/gawk/) with a custom `FS`, or more specialized parsers like [Perl](https://www.perl.org/)/[Python](https://www.python.org/) scripts, or [jq](https://stedolan.github.io/jq/) for JSON logs), but for many [NGINX](https://nginx.org/en/docs/) access logs a careful use of [awk](https://www.gnu.org/software/gawk/) field indices (as shown) is sufficient.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/devops-interview-prep/module/370000ef-b6bc-4986-8d29-0793ebb2c9e7/lesson/61056487-8d7d-4846-a026-c5681731ee9e" />
</CardGroup>
