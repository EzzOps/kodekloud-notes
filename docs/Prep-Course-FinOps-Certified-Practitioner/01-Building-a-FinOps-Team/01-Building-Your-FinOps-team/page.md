# List Cilium agent pods (namespace may vary)
kubectl -n kube-system get pods -l k8s-app=cilium

# Tail logs for a Cilium agent
kubectl -n kube-system logs <cilium-agent-pod> -c cilium --tail=200
```

Representative log lines you may see:

```bash theme={null}
level=info msg="Policy requires authentication for connection" source="policy"
level=info msg="Auth table miss; dropping initial packet and triggering auth" source="ebpf"
level=info msg="Requesting SVID from local Spire agent" source="cilium-agent"
level=info msg="TLS session established between agents, auth cache updated" source="tls-session-manager"
```

To inspect SPIRE components:

```bash theme={null}
kubectl -n cilium-spire logs spire-server-0 -c spire-server
kubectl -n cilium-spire logs spire-agent-cx9h6 -c spire-agent
```

These logs reveal SVID issuance, agent handshakes, and other details of identity issuance and renewal.

## Troubleshooting checklist

* Confirm encryption (IPsec/WireGuard) is enabled.
* Verify Spire server and agents are running in the cluster.
* Ensure Cilium has authentication.mutual.spire.enabled set to true.
* Check Cilium agent logs for auth/table misses and TLS session events.
* Inspect spire-server and spire-agent logs for SVID issuance problems.
* Confirm your CiliumNetworkPolicy matches the correct endpoints and ports.

## Summary

* Cilium implements mTLS using SPIFFE identities and SPIRE as a common SPIFFE implementation.
* Mutual authentication happens at the Cilium agent level; pods do not perform certificate exchange.
* Enable encryption and authentication in your Cilium configuration and deploy SPIRE (or let Cilium install it).
* Protect traffic by creating a CiliumNetworkPolicy with authentication.mode: required.
* Use Cilium and SPIRE logs to observe and debug the authentication flow.

Further reading and references:

* [Cilium Documentation](https://docs.cilium.io/)
* [SPIFFE](https://spiffe.io/)
* [SPIRE](https://spiffe.io/spire/)
* [eBPF](https://ebpf.io/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/cilium-certified-associate-cca/module/50bb84d0-61e7-4f73-a51b-7da0e8338438/lesson/834012c3-3c5b-47cb-bfee-1cf373732e3d)


# Building Your FinOps team

Source: https://notes.kodekloud.com/docs/Prep-Course-FinOps-Certified-Practitioner/Building-a-FinOps-Team/Building-Your-FinOps-team/page

Guide to building a cross-functional FinOps team that decentralizes cloud cost ownership, centralizes governance, defines roles and scaling, and outlines practical first steps and a 90-day pilot.

Welcome — this lesson is the first step toward building a high-impact FinOps capability. By the end you'll understand why a dedicated FinOps capability matters, how to structure it for maximum impact, and practical first steps to get started.

FinOps is not just about hiring finance people. It's a cross-functional capability that bridges finance, engineering, and product operations — think of it as assembling your cloud cost-optimization Avengers. The organizational shift a proper FinOps capability delivers is simple but powerful: decentralize day-to-day accountability while centralizing macro-level functions.

Key distinctions:

* Decentralized accountability: give product and engineering teams ownership of the cloud costs they consume so they can optimize in real time. Empower teams to make decisions and provide curated, actionable insights at the team level.
* Centralized macro functions: deliver organization-wide insights, alignment to business strategy, governance, frameworks, and coordination across teams.

<Frame>
  <img alt="The image describes building a FinOps team, contrasting centralized control with decentralized accountability using green and red arrows with thumbs up and down. Key points include macro-level insights, strategic alignment, empowered teams, and curated insights." />
</Frame>

Think of the model as an orchestra: each team (musician) plays its own instrument while a central FinOps function (the conductor) ensures everyone performs the same symphony.

Starting a FinOps program can feel overwhelming. That’s normal. No organization gets its structure perfect on day one. Adopt an iterative mindset: start small, measure impact, and scale the capability as your cloud spend and organizational complexity grow.

> **lightbulb** Start with a minimum-viable FinOps capability, measure impact, then evolve structure and roles as your spend and complexity grow.

## Five Fundamental Questions for Building a FinOps Team

Below are five practical questions every organization should answer when creating a FinOps capability. These guide rails are useful for heads of product, engineering leads, and engineering managers.

| Question                                | Practical guidance                                                                                                                                                                                                                                              |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Who should be in the FinOps team?       | Look beyond job titles. Include people who influence cloud spend today: cloud architects, senior developers, product managers, finance reps, and ops engineers. Often the best contributors are engineers who consistently ask, “Why does this cost so much?”   |
| What roles fit the organization?        | Align roles to how your company operates: startups often need multi-hat contributors; mid-size orgs benefit from roles like FinOps engineer, cloud financial analyst, and business value manager; enterprises need layered teams for governance and enablement. |
| How many people are needed?             | Use a minimum-viable-team approach: start with 2–3 people and scale with spend/complexity. A rough guideline: \~1 dedicated FinOps person per \$10M annual cloud spend, counting full- and part-time contributors.                                              |
| What should reporting look like?        | Report into a leader with influence across tech and finance (CTO, CFO, or COO). This reporting line empowers FinOps to remove blockers and drive cross-functional change.                                                                                       |
| What are the barriers to effectiveness? | Identify cultural, technical, and organizational blockers early (e.g., lack of billing access, unclear ownership, misaligned incentives), then create a plan to remove or mitigate them.                                                                        |

### Who should be on the team?

* Identify people who already influence cost decisions: cloud architects, senior engineers, product managers, finance partners, and SREs.
* Include domain experts who can translate cost signals into product and engineering trade-offs.
* Promote practitioner-level FinOps skills (tagging, usage attribution, rightsizing) alongside financial literacy.

### Typical roles and responsibilities

| Role                           |                                 Primary responsibility | Typical in     |
| ------------------------------ | -----------------------------------------------------: | -------------- |
| FinOps Engineer                |       Implement tooling, tagging, reporting automation | Mid/Enterprise |
| Cloud Financial Analyst        |        Analyze spend, forecasting, showback/chargeback | Mid/Enterprise |
| Business Value Manager         | Align cost optimization with product/business outcomes | Mid/Enterprise |
| Cross-functional Practitioners |  Developers/archs who own team-level cost optimization | All sizes      |

### How many people?

Start with a small corps of dedicated contributors and a broader set of part-time collaborators embedded in product and engineering teams. Use workload and spend as scaling signals.

### Where should FinOps report?

Reporting into a leader who can influence both finance and engineering (CTO/CFO/COO) helps with authority and cross-functional execution. If separate reporting is unavoidable, create strong sponsorship and a clear charter.

> **warning** Common blockers include poor access to billing and usage data, unclear ownership of cost outcomes, and incentives that favor feature velocity over cost efficiency. Address these early to unlock results.

<Frame>
  <img alt="The image focuses on building a FinOps team and lists questions about team composition and effectiveness. It features a person appearing thoughtful next to these points." />
</Frame>

## Practical next steps (minimum viable plan)

1. Assemble a core team of 2–3 people (mix of engineering and finance).
2. Lock down access to billing, tagging, and usage data.
3. Define team-level cost ownership and simple KPIs (e.g., monthly spend per feature, rightsizing actions).
4. Run a 90-day pilot focused on one product area to prove ROI.
5. Document playbooks and scale to additional teams based on demonstrated impact.

## Where to go next

Later lessons in this series will show concrete team examples for startups, mid-size firms, and large enterprises along with sample org charts, hiring profiles, and playbooks.

Further reading:

* FinOps Foundation — [https://www.finops.org/](https://www.finops.org/)
* Cloud cost optimization principles — [https://cloud.google.com/architecture/cost-optimization](https://cloud.google.com/architecture/cost-optimization) (example reference)

Thanks for reading.

- [Watch Video](https://learn.kodekloud.com/user/courses/finops-certified-practitioner/module/1de0a7cc-5e70-4e69-a8f4-f8c83d2b45fc/lesson/1f67578c-94e9-4cac-a9ba-a070d3c12378)
