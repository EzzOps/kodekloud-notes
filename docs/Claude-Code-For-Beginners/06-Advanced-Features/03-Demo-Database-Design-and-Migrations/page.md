# Configuration
PROFILE_NAME="demo"
NODES=3
CPU=2
MEM=4096

# Determine non-root user (when run with sudo)
TARGET_USER="${SUDO_USER:-$USER}"

# Update package list
sudo apt-get update -y

# Install prerequisites
sudo apt-get install -y ca-certificates curl gnupg apt-transport-https \
    conntrack socat ebtables ethtool

# Configure kernel modules and sysctls
sudo modprobe br_netfilter || true
echo "net.bridge.bridge-nf-call-iptables=1" | sudo tee /etc/sysctl.d/99-k8s.conf >/dev/null
echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.d/99-k8s.conf >/dev/null
sudo sysctl --system

# Install Docker (idempotent)
if ! command -v docker >/dev/null 2>&1; then
    sudo apt-get install -y docker.io
    sudo systemctl enable --now docker
    # Add the non-root user (or current user) to the docker group
    sudo usermod -aG docker "$TARGET_USER" || true
fi

# Install kubectl (using official packages)
if ! command -v kubectl >/dev/null 2>&1; then
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.34/deb/Release.key \
        | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
    echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.34/deb/ /" \
        | sudo tee /etc/apt/sources.list.d/kubernetes.list
    sudo apt-get update -y
    sudo apt-get install -y kubectl
fi

# Install Minikube (idempotent)
if ! command -v minikube >/dev/null 2>&1; then
    curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube /usr/local/bin/minikube
    rm -f minikube
fi

# Start Minikube profile if it doesn't exist
if ! minikube profile list -o=json | grep -q "\"Name\": \"$PROFILE_NAME\""; then
    # Start minikube using the docker driver
    minikube start -p "$PROFILE_NAME" --driver=docker --nodes="$NODES" --cpus="$CPU" --memory="$MEM"
else
    echo "Minikube profile \"$PROFILE_NAME\" already exists; skipping start."
fi

# Enable addons (run under docker group context if necessary)
# Some addon operations may require being in the docker group context
if ! minikube -p "$PROFILE_NAME" addons list | grep -q "metrics-server.*enabled"; then
    newgrp docker <<'EOFF'
minikube -p "$PROFILE_NAME" addons enable metrics-server || true
minikube -p "$PROFILE_NAME" addons enable ingress || true
minikube -p "$PROFILE_NAME" addons enable dashboard || true
EOFF
fi

# Deploy demo app if not present
if ! kubectl get deploy hello >/dev/null 2>&1; then
    kubectl create deployment hello --image=nginx --port=80
    kubectl expose deployment hello --type=NodePort --port=80
fi

# Final status output
echo "=== Nodes ==="
kubectl get nodes -o wide || true

echo
echo "=== Services ==="
kubectl get svc -o wide || true

echo
echo "=== Demo URL(s) ==="
minikube -p "$PROFILE_NAME" service hello --url || true

echo
echo "Fallback (port-forward from this VM):"
echo "  kubectl port-forward deploy/hello 8080:80"
echo "Then curl http://localhost:8080"
```

Make the script executable and run it:

```bash theme={null}
chmod +x /tmp/minikube-demo.sh
/tmp/minikube-demo.sh
```

4 — Handling Docker group and add-ons

When the installer adds your user to the docker group, the membership may not take effect until you start a new login shell. The generated script attempts to enable add-ons inside a `newgrp docker` subshell to avoid permission errors. If an add-on fails due to permissions, re-run the add-on commands after obtaining docker group privileges:

```bash theme={null}
# Ensure the current shell has docker group privileges, then:
newgrp docker
minikube -p demo addons enable metrics-server
minikube -p demo addons enable ingress
minikube -p demo addons enable dashboard
```

> **warning** If you do not start a new shell or run `newgrp docker`, Minikube or addon commands may fail with permission errors. Log out and log back in, or use `newgrp docker`, before re-running addon commands.

5 — Test the demo application (port-forward)

Quick port-forward test from the VM:

```bash theme={null}
kubectl port-forward deploy/hello 8080:80 &
PF_PID=$!
sleep 2
curl -s http://localhost:8080 | head -n 5
kill "$PF_PID" 2>/dev/null || true
```

Alternatively, use the Minikube-provided service URL printed by the script:

```bash theme={null}
minikube -p demo service hello --url
```

6 — Expected result summary

After the script runs successfully you should see:

| Component | What to expect                                                                                   |
| --------: | ------------------------------------------------------------------------------------------------ |
|   Prereqs | ca-certificates, curl, gnupg, apt-transport-https, conntrack, socat, ebtables, ethtool installed |
|   Sysctls | net.bridge.bridge-nf-call-iptables=1 and net.ipv4.ip\_forward=1 applied                          |
|    Docker | Installed, enabled, and user added to docker group                                               |
|   kubectl | Installed from the official pkgs.k8s.io repository                                               |
|  Minikube | Installed and a 3-node Minikube profile named "demo" started (Docker driver)                     |
|   Add-ons | metrics-server, ingress, dashboard enabled (if permissions allow)                                |
|  Demo app | "hello" nginx Deployment created and exposed as a NodePort service                               |
|    Access | Demo URL(s) printed and a port-forward fallback provided                                         |

Example verification console snippets you may see:

```text theme={null}
Forwarding from 127.0.0.1:8080 -> 80
Forwarding from [::1]:8080 -> 80
Handling connection for 8080
```

and

```text theme={null}
=== Nodes ===
NAME                 STATUS   ROLES    AGE   VERSION
demo-m01             Ready    control-plane   2m    v1.33.1
demo-m02             Ready    <none>          2m    v1.33.1
demo-m03             Ready    <none>          2m    v1.33.1

=== Services ===
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
hello        NodePort    10.96.0.123      <none>        80:31902/TCP   1m

=== Demo URL(s) ===
http://192.168.49.2:31902
```

Notes and tips

> **lightbulb** Running the full three-node demo on a single VM requires sufficient host resources. If you have limited RAM/CPU, reduce NODES or MEM in the script (for example, use 1 node or 2GB per node) to test locally. Also consider using fewer add-ons while troubleshooting.

Quick checklist (sanity checks)

* Ensure the VM has enough RAM and CPUs for the configured node count.
* Confirm internet connectivity for package and image downloads.
* If kubectl or minikube fail unexpectedly, inspect logs and retry after ensuring docker group membership is active.

Links and references

* [Claude Code For Beginners (KodeKloud course)](https://learn.kodekloud.com/user/courses/claude-code-for-beginners)
* [Kubernetes Documentation — Concepts](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* Minikube: [https://minikube.sigs.k8s.io/](https://minikube.sigs.k8s.io/)
* Docker: [https://docs.docker.com/](https://docs.docker.com/)
* pkgs.k8s.io (kubectl packages): [https://pkgs.k8s.io/](https://pkgs.k8s.io/)

This lesson demonstrates how a single clear, structured prompt to Claude Code can produce an automated, idempotent script that reduces manual setup time for local Kubernetes testing with Minikube.

- [Watch Video](https://learn.kodekloud.com/user/courses/claude-code-for-beginners/module/a295c914-f61e-47bb-8adc-7a3145745aa6/lesson/43ada54a-3944-4d25-8e4a-252597dc38c3)


# Demo Database Design and Migrations

Source: https://notes.kodekloud.com/docs/Claude-Code-For-Beginners/Advanced-Features/Demo-Database-Design-and-Migrations/page

Migrating a MariaDB contacts table into a single-file SQLite database using a Python script with schema mapping, safe parameterized imports, auditing SQL artifacts, and verification.

This lesson demonstrates migrating a small MariaDB database into a single-file SQLite database. The goal is to read schema and data from a local MariaDB instance and produce a SQLite file containing the same records and an approximation of the schema — suitable for low-traffic or archival databases where the operational overhead of running MariaDB is unnecessary.

We use a compact, iterative workflow: start with a concise prompt to generate an approach, then expand to a reproducible Python script when the quick approach is brittle.

<Frame>
  <img alt="A dark-themed database application window showing a &#x22;contacts&#x22; table with columns like id, first name, last name, job title and email. The left sidebar shows the database/server tree while the main pane lists many contact rows." />
</Frame>

## Scenario

* Source: local MariaDB server with a contacts table (id, first\_name, last\_name, job\_title, email).
* Target: a single SQLite database file (contacts.db) containing the same rows and a mapped schema.
* Motivation: reduce operational complexity for small/low-traffic databases by moving to SQLite.

Primary objectives:

* Detect schema and map types with sensible defaults.
* Export rows safely and import into SQLite using parameterized inserts.
* Produce .sql artifacts for auditing and replay.
* Verify migration (row counts and spot checks).

## Prompt‑first workflow

1. Try a concise instruction and let the model propose a plan.
2. If that plan is brittle or incomplete, request a production-quality script (Python) implementing:
   * Schema discovery (INFORMATION\_SCHEMA),
   * Type affinity mapping,
   * Safe data export/import with parameterized queries,
   * Optional CLI args and logging,
   * Simple verification (row counts),
   * Optional output .sql files for auditing.

Example concise prompt used:

```text theme={null}
I want to migrate my database from a local MariaDB server to a SQLite database and have the data moved from the MariaDB server to the SQLite database.
```

If you prefer a prescriptive, production-ready specification, the later detailed prompt included environment, language, CLI args, and migration steps.

## Example detailed requirements (used to generate the final script)

* Environment & dependencies:
  * Language: Python 3.10+
  * Connectors: mysql-connector-python (or pymysql) + stdlib sqlite3
  * Optional: click (CLI), tqdm (progress), tenacity (retries)
* Script requirements:
  * Run locally; accept connection via CLI args or environment variables
  * Detect server version and charset
  * Discover schema: tables, columns, nullability, defaults
  * Primary keys/unique keys/indexes; document foreign keys, views, triggers
  * Export data safely and import into SQLite with parameterized queries
  * Emit .sql artifacts for auditing/replay
* CLI args (examples):
  \--mysql-host, --mysql-port, --mysql-user, --mysql-password, --mysql-db
  \--sqlite-path, --output-dir, --force-overwrite

## MariaDB → SQLite: Type mapping (approximate)

| MariaDB types                                 | Suggested SQLite affinity / representation           |
| --------------------------------------------- | ---------------------------------------------------- |
| INT / BIGINT / MEDIUMINT / SMALLINT / TINYINT | INTEGER                                              |
| TINYINT(1) used as boolean                    | INTEGER (0/1)                                        |
| DECIMAL(p,s), NUMERIC                         | NUMERIC                                              |
| FLOAT / DOUBLE                                | REAL                                                 |
| BIT                                           | INTEGER (0/1) or BLOB if wide                        |
| CHAR / VARCHAR / TEXT / ENUM / SET            | TEXT                                                 |
| BINARY / VARBINARY / BLOB                     | BLOB                                                 |
| DATE / DATETIME / TIMESTAMP / TIME / YEAR     | TEXT (ISO formats: YYYY-MM-DD / YYYY-MM-DD HH:MM:SS) |

Note: SQLite uses type affinity, so these are pragmatic mappings rather than exact conversions. Document and review columns with special constraints (e.g., unsigned integers, auto-increment semantics).

## Practical run — repository inspection and initial interaction

The model inspected repository files (contacts CSV, contacts\_data.sql, migration.md) and asked for connection info. Never share production credentials in untrusted environments — use a local test account or pass secrets at runtime.

> **lightbulb** Do not share production credentials or secrets in an environment you do not control. Use local test credentials or create scripts that accept credentials at runtime (environment variables or interactive input) rather than embedding secrets in chat history or files.

Sample connection details used interactively for testing:

```text theme={null}
Host: localhost
Port: 3306
Database name: contactsdb
Username: jeremy
Password: password123
Table name: contacts
```

## Initial inspection & mysqldump

Quick inspection commands the model proposed:

Inspect table schema:

```bash theme={null}
mysql -h localhost -u jeremy -ppassword123 contactsdb -e "DESCRIBE contacts;"
```

Export schema + data using mysqldump for auditing / replay:

```bash theme={null}
mysqldump -h localhost -u jeremy -ppassword123 --no-create-db --single-transaction contactsdb contacts > contacts_data.sql
```

Excerpt from contacts\_data.sql (example):

```sql theme={null}
DROP TABLE IF EXISTS `contacts`;
CREATE TABLE `contacts` (
  `id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `job_title` varchar(100) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
...
INSERT INTO `contacts` VALUES
(1,'Britt','Hyne','Senior Editor','bhyne@lulu.com'),
(2,'Merrel','Cornew','VP Product Management','mcornew1@indiegogo.com'),
...
(1000,'Enos','Dalliston','Nurse Practitioner','edallistonrr@mozilla.com');
```

## Why quick shell-based piping is brittle

A naive pipeline that reads mysql tab-separated output and pipes it into sqlite3 (with sed and shell parsing) often fails on real data: names with apostrophes, embedded tabs, newline characters in text fields, or other quoting issues break the parsing and produce invalid SQL.

Example brittle approach (DO NOT use in production):

```bash theme={null}
mysql -h localhost -u jeremy -ppassword123 contactsdb -e "SELECT * FROM contacts;" \
  | sed 's/\t/|/g' | tail -n +2 \
  | while IFS='|' read -r id first_name last_name job_title email; do
      sqlite3 contacts.db "INSERT INTO contacts (id, first_name, last_name, job_title, email) VALUES ('$id', '$first_name', '$last_name', '$job_title', '$email');"
    done
```

Common failure: apostrophes in names (e.g., O'Connolly) or embedded separators break quoting and allow SQL injection.

## Safer approach: Python migration script with parameterized queries

A robust approach uses a Python script that:

* Reads rows via a MariaDB client (mysql-connector-python or pymysql),
* Inserts rows into SQLite using parameterized queries to avoid quoting/injection issues,
* Creates a minimal SQLite schema with mapped types,
* Optionally writes .sql files for auditing.

Concise example of migrate.py used for the contacts table:

```python theme={null}
#!/usr/bin/env python3
"""
migrate.py - simple migration of the 'contacts' table from MariaDB to SQLite.

Usage: configure connection details below or adapt to accept CLI args / env vars.
"""
import sqlite3
import mysql.connector
import sys
