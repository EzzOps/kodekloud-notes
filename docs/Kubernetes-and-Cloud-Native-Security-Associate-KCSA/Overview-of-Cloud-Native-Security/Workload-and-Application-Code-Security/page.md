# Workload and Application Code Security

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Overview-of-Cloud-Native-Security/Workload-and-Application-Code-Security/page

This guide covers securing application code through secure coding patterns, dependency scanning, runtime protection, and observability for resilient software development.

As we’ve secured the cloud, the cluster, and containers, the next step is hardening your application code. This guide covers four critical areas—secure coding patterns, dependency scanning, runtime protection, and observability—to help you build resilient, production-ready software.

## 1. Preventing SQL Injection

SQL injection remains one of the most prevalent vulnerabilities. Malicious input can tamper with your database queries, leading to data leakage or unauthorized access.

### Vulnerable Query Example

```sql theme={null}
SELECT * FROM users
WHERE username = 'user_input'
  AND password = 'password_input';
```

An attacker could supply `'' OR '1'='1'` as the username and bypass authentication entirely:

```sql theme={null}
SELECT * FROM users
WHERE username = '' OR '1'='1'
  AND password = '';
```

### Secure Mitigation

Always use parameterized queries or prepared statements:

```python theme={null}
