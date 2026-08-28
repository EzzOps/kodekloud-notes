# KodeKloud Notes Archive

Complete mirror of [notes.kodekloud.com](https://notes.kodekloud.com) documentation — 9168 pages across 180 courses covering Kubernetes, Cloud Native, DevOps, AWS, Azure, GCP, and Platform Engineering.

## 📊 Stats

- **9,168 pages** of course content
- **180 courses** covering:
  - Kubernetes (CKA, CKAD, CKS)
  - Cloud platforms (AWS, Azure, GCP)
  - DevOps tools (Terraform, Ansible, Jenkins, ArgoCD)
  - Platform Engineering & CNCF ecosystem
  - AI/ML fundamentals and certifications
- **125 MB** of markdown documentation
- **Last updated:** 2026-08-28

## 📁 Structure

```
docs/
├── 12-Factor-App/
├── AI-Agents/
├── AWS-Certified-Developer-Associate/
├── Certified-Kubernetes-Administrator-CKA/
├── Docker-Training-Course-for-the-Absolute-Beginner/
├── Terraform-for-Beginners/
└── ... (180 courses total)
```

Each course maintains the original hierarchy:
```
docs/Course-Name/
├── Module-1/
│   ├── Topic-1/
│   │   └── page.md
│   └── Topic-2/
│       └── page.md
└── Module-2/
    └── ...
```

## 🔍 Quick Search

Use GitHub's search or `grep` to find content:

```bash
# Find all Kubernetes networking content
grep -r "kubernetes networking" docs/

# Search specific course
grep -r "pod security" docs/Certified-Kubernetes-Administrator-CKA/

# List all courses
ls -1 docs/
```

## 📚 Featured Courses

### Kubernetes
- [Certified Kubernetes Administrator (CKA)](docs/Certified-Kubernetes-Administrator-CKA/)
- [Certified Kubernetes Application Developer (CKAD)](docs/Certified-Kubernetes-Application-Developer-CKAD/)
- [Certified Kubernetes Security Specialist (CKS)](docs/Certified-Kubernetes-Security-Specialist-CKS/)
- [Ultimate CKA Mock Exam Series](docs/Ultimate-Certified-Kubernetes-Administrator-CKA-Mock-Exam-Series/)

### AWS
- [AWS Certified Developer Associate](docs/AWS-Certified-Developer-Associate/)
- [AWS Solutions Architect Associate](docs/AWS-Solutions-Architect-Associate-Certification/)
- [AWS CloudFormation](docs/AWS-CloudFormation/)
- [AWS EKS](docs/AWS-EKS/)

### DevOps & Platform Engineering
- [Fundamentals of DevOps](docs/Fundamentals-of-DevOps/)
- [Fundamentals of SRE](docs/Fundamentals-of-SRE/)
- [Terraform for Beginners](docs/Terraform-for-Beginners/)
- [Jenkins Pipelines](docs/Jenkins-Pipelines/)

### CNCF Ecosystem
- [ArgoCD (Certified Argo Project Associate)](docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/)
- [Cilium (Certified Cilium Associate)](docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/)
- [Istio Service Mesh](docs/Istio-Service-Mesh/)
- [Prometheus Certified Associate](docs/Prometheus-Certified-Associate-PCA/)

### AI/ML
- [AI Agents](docs/AI-Agents/)
- [AI Assisted Development](docs/AI-Assisted-Development/)
- [AWS Certified AI Practitioner](docs/AWS-Certified-AI-Practitioner/)
- [Fundamentals of MLOps](docs/Fundamentals-of-MLOps/)

## 🛠️ Build Process

This archive was built by parsing KodeKloud's official `llms-full.txt` endpoint:

```python
# Download and split into organized repo
curl https://notes.kodekloud.com/llms-full.txt
# Parse by "Source: URL" markers
# Save to docs/Course/Module/Topic/page.md
```

## 📖 Usage

### Browse locally
```bash
git clone https://github.com/EzzOps/kodekloud-notes.git
cd kodekloud-notes
find docs/ -name "*.md" | fzf
```

### Search specific topic
```bash
# Find all ArgoCD content
grep -r "argocd" docs/ | less

# Find exam tips
grep -r "exam tip" docs/Certified-Kubernetes-Administrator-CKA/
```

### Build local search index
```bash
# Using ripgrep for fast search
rg "pod security policy" docs/
```

## 🔗 Links

- Official site: [notes.kodekloud.com](https://notes.kodekloud.com)
- KodeKloud Learning Platform: [learn.kodekloud.com](https://learn.kodekloud.com)
- LLM-friendly index: [llms.txt](https://notes.kodekloud.com/llms.txt)

## ⚖️ License

This is a mirror of publicly available KodeKloud educational content. All course materials are © KodeKloud. This archive is provided for educational reference and offline access.

## 🤝 Contributing

Found issues or want to update content?
- Report broken links or formatting issues via GitHub Issues
- To update content, re-run the parser against latest llms-full.txt

## 📅 Update Schedule

This archive snapshots KodeKloud notes as of **2026-08-28**. To refresh:

```bash
python3 scripts/kodekloud-parser.py
```

---

**Built with ❤️ for the Platform Engineering community**

[⭐ Star this repo](https://github.com/EzzOps/kodekloud-notes) if you find it useful!
