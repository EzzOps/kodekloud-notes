# Container Data Bind Mounts vs Volumes

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Docker/Container-Data-Bind-Mounts-vs-Volumes/page

Comparison of Docker bind mounts and named volumes for persisting container data, use cases and production considerations.

How do you persist the data a container produces?

Containers are ephemeral by design: when a container is removed, anything stored only inside it is lost. To persist data reliably you must place it outside the container’s writable layer. Two common approaches are bind mounts and named volumes. Choosing the right one affects development workflow, portability, and production reliability.

Below we compare both approaches, explain typical use cases, and show simple examples.

## Option 1 — Bind mounts (host directory mounted into container)

With a bind mount you attach a specific folder on the host into the container. Anything written by the container to that mount goes directly into the host folder. This is convenient for local development because you can edit code on your machine and the running container immediately sees those changes.

<Frame>
  <img alt="The image explains &#x22;Bind Mounts&#x22; with a diagram showing a connection between a host machine and a container, emphasizing local development where code edits are instantly reflected in the container." />
</Frame>

Example: mount a host directory into the container

```bash theme={null}
