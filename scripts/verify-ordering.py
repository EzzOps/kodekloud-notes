#!/usr/bin/env python3
"""Verify course module/lesson ordering is correct."""
import sys
from pathlib import Path

REPO_ROOT = Path("/opt/data/kodekloud-notes/repo")
DOCS_DIR = REPO_ROOT / "docs"

COURSE_MODULE_ORDER = {
    "Helm-for-Beginners": ["Introduction", "Introduction-to-Helm", "Helm-Charts-Anatomy", "Conclusion"],
    "Docker-Training-Course-for-the-Absolute-Beginner": ["Introduction", "Docker-Commands", "Docker-Images", "Docker-Networking", "Docker-Run", "Docker-Compose", "Docker-Engine-Storage", "Docker-Registry", "Docker-on-Mac-Windows", "Container-Orchestration-Docker-Swarm-Kubernetes", "Conclusion"],
    "12-Factor-App": ["Introduction", "Twelve-Factor-App-methodology", "Conclusion"],
    "Enhancing-Soft-Skills-for-DevOps-Engineers-Essential-Non-Technical-Skills-to-Thrive": ["Introduction", "Communication-Expression-and-Storytelling", "Growing-Learning-and-Adapting-to-Change", "Priority-Time-and-Capacity-Management", "Influencing-Persuasion-and-Leadership", "Consulting-and-Client-Management", "Conclusion"],
    "AWS-Solutions-Architect-Associate-Certification": ["Introduction", "Services-Networking", "Services-Application-Integration", "Services-Compute", "Services-Data-and-ML", "Services-Database", "Services-Storage", "Bringing-it-all-together", "Designing-for-Security", "Services-Management-and-Governance", "Services-Migration-and-Transfer", "Services-Security", "Applying-your-Design-Skills", "Designing-for-Cost-Optimization", "Designing-for-Performance", "Designing-for-Reliability"],
    "Certified-Kubernetes-Administrator-CKA": ["Introduction", "Core-Concepts", "Application-Lifecycle-Management", "Cluster-Maintenance", "Logging-Monitoring", "Networking", "Scheduling", "Security", "Storage", "Troubleshooting", "Design-and-Install-a-Kubernetes-Cluster", "Helm-Basics-2025-Updates", "Install-Kubernetes-the-kubeadm-way", "Kustomize-Basics-2025-Updates", "Mock-Exams"],
}

def extract_name(dir_name):
    """Extract the name part after the numeric prefix."""
    if '-' in dir_name:
        return dir_name.split('-', 1)[1]
    return dir_name

def verify_course(course_dir):
    course_name = course_dir.name
    if course_name not in COURSE_MODULE_ORDER:
        return True, []
    
    expected_modules = COURSE_MODULE_ORDER[course_name]
    actual_modules = [extract_name(d.name) for d in sorted(course_dir.iterdir()) if d.is_dir()]
    
    errors = []
    if actual_modules != expected_modules:
        errors.append(f"Module order mismatch for {course_name}:")
        errors.append(f"  Expected: {expected_modules}")
        errors.append(f"  Actual:   {actual_modules}")
        return False, errors
    
    return True, []

def main():
    all_ok = True
    all_errors = []
    
    for course_dir in sorted(DOCS_DIR.iterdir()):
        if course_dir.is_dir() and course_dir.name in COURSE_MODULE_ORDER:
            ok, errors = verify_course(course_dir)
            if not ok:
                all_ok = False
                all_errors.extend(errors)
            else:
                print(f"✓ {course_dir.name}: Module order OK")
    
    if all_ok:
        print("\n✅ All verified courses have correct module ordering!")
        return 0
    else:
        print("\n❌ Ordering issues found:")
        for e in all_errors:
            print(e)
        return 1

if __name__ == "__main__":
    sys.exit(main())
