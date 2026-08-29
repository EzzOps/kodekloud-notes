# Demo Rate Limiting

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Performance/Demo-Rate-Limiting/page

Guide demonstrating NGINX request and connection rate limiting using limit_req and limit_conn, with testing, configuration examples, tuning, and logs

This lesson demonstrates NGINX rate limiting using two mechanisms:

* Request rate limiting (`limit_req`) — controls how many requests a client (usually per-IP) can make over time.
* Connection limiting (`limit_conn`) — caps the number of simultaneous connections from a client.

First we'll show the server behavior with no limits, then add request and connection limits and observe the effects using `curl` and ApacheBench (`ab`).

A diagram illustrating per-IP request and connection limits appears below and is referenced throughout the examples.

<Frame>
  <img alt="A diagram showing a server (IP 192.230.8.10) sending multiple requests to https://www.example.com via NGINX. It illustrates per-IP rate and connection limits with green check marks for allowed requests and red crosses for blocked ones." />
</Frame>

## 1) Smoke test (no rate limiting)

Begin by verifying basic connectivity from your client node (for example `node01`). Map the server IP in `/etc/hosts` so you can reach the site by name, then perform a simple request:

```bash theme={null}
