#!/usr/bin/env python3
"""
Fix KodeKloud course ordering and image paths.
- Reorder modules/lessons to match actual KodeKloud course sequence
- Fix broken image paths to be relative/local
"""

import os
import re
import shutil
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path("/opt/data/kodekloud-notes/repo")
DOCS_DIR = REPO_ROOT / "docs"
IMAGES_DIR = REPO_ROOT / "images"

# Known correct module ordering for courses (module_name -> order_index)
# This maps the URL module name to its correct position in the course
COURSE_MODULE_ORDER = {
    # Helm-for-Beginners
    "Helm-for-Beginners": {
        "Introduction": 1,
        "Introduction-to-Helm": 2,
        "Helm-Charts-Anatomy": 3,
        "Conclusion": 4,
    },
    # Docker-Training-Course-for-the-Absolute-Beginner
    "Docker-Training-Course-for-the-Absolute-Beginner": {
        "Introduction": 1,
        "Docker-Commands": 2,
        "Docker-Images": 3,
        "Docker-Networking": 4,
        "Docker-Run": 5,
        "Docker-Compose": 6,
        "Docker-Engine-Storage": 7,
        "Docker-Registry": 8,
        "Docker-on-Mac-Windows": 9,
        "Container-Orchestration-Docker-Swarm-Kubernetes": 10,
        "Conclusion": 11,
    },
    # 12-Factor-App
    "12-Factor-App": {
        "Introduction": 1,
        "Twelve-Factor-App-methodology": 2,
        "Conclusion": 3,
    },
    # Enhancing-Soft-Skills-for-DevOps-Engineers-Essential-Non-Technical-Skills-to-Thrive
    "Enhancing-Soft-Skills-for-DevOps-Engineers-Essential-Non-Technical-Skills-to-Thrive": {
        "Introduction": 1,
        "Communication-Expression-and-Storytelling": 2,
        "Growing-Learning-and-Adapting-to-Change": 3,
        "Priority-Time-and-Capacity-Management": 4,
        "Influencing-Persuasion-and-Leadership": 5,
        "Consulting-and-Client-Management": 6,
        "Conclusion": 7,
    },
    # AWS-Solutions-Architect-Associate-Certification
    "AWS-Solutions-Architect-Associate-Certification": {
        "Introduction": 1,
        "Services-Networking": 2,
        "Services-Application-Integration": 3,
        "Services-Compute": 4,
        "Services-Data-and-ML": 5,
        "Services-Database": 6,
        "Services-Storage": 7,
        "Bringing-it-all-together": 8,
        "Designing-for-Security": 9,
        "Services-Management-and-Governance": 10,
        "Services-Migration-and-Transfer": 11,
        "Services-Security": 12,
        "Applying-your-Design-Skills": 13,
        "Designing-for-Cost-Optimization": 14,
        "Designing-for-Performance": 15,
        "Designing-for-Reliability": 16,
    },
    # Certified-Kubernetes-Administrator-CKA
    "Certified-Kubernetes-Administrator-CKA": {
        "Introduction": 1,
        "Core-Concepts": 2,
        "Application-Lifecycle-Management": 3,
        "Cluster-Maintenance": 4,
        "Logging-Monitoring": 5,
        "Networking": 6,
        "Scheduling": 7,
        "Security": 8,
        "Storage": 9,
        "Troubleshooting": 10,
        "Design-and-Install-a-Kubernetes-Cluster": 11,
        "Helm-Basics-2025-Updates": 12,
        "Install-Kubernetes-the-kubeadm-way": 13,
        "Kustomize-Basics-2025-Updates": 14,
        "Mock-Exams": 15,
    },
}


def get_module_order(course_name, module_name):
    """Get the correct order index for a module within a course."""
    if course_name in COURSE_MODULE_ORDER:
        return COURSE_MODULE_ORDER[course_name].get(module_name, 999)
    return 999


def get_lesson_order(course_name, module_name, lesson_name):
    """Get the correct order index for a lesson within a module."""
    # Common lesson orderings per module type
    lesson_orders = {
        "Introduction": {
            "Introduction": 1,
            "Course-Introduction": 1,
            "Why-take-this-course": 2,
            "Why-12-Factor-app": 2,
            "A-Quick-Reminder": 2,
            "Demo-Setup-and-Install-Docker": 3,
            "Docker-Overview": 4,
            "Getting-started-with-Docker": 5,
            "Module-Introduction": 1,
            "Certification-Details": 2,
            "Course-Introduction": 1,
            "Introduction-and-Problems-this-course-solves": 1,
            "What-Is-Artificial-Intelligence": 1,
            "Responsible-AI-Considerations": 2,
            "Azure-AI-Services": 3,
            "Azure-Machine-Learning": 4,
            "Azure-AI-Search": 5,
            "Deploying-Azure-AI-Services": 1,
            "Working-with-Azure-AI-Services": 2,
            "Module-Introduction": 1,
        },
        "Conclusion": {
            "Conclusion": 1,
            "Bonus-Lecture-Introduction-to-YAML": 1,
        },
        "Docker-Commands": {
            "Basic-Docker-Commands": 1,
            "Demo-Docker-Commands": 2,
        },
        "Docker-Images": {
            "Commands-vs-Entrypoint": 1,
            "Docker-Images": 2,
            "Demo-Creating-a-new-Docker-Image": 3,
            "Environment-Variables": 4,
        },
        "Docker-Networking": {
            "Docker-Networking": 1,
        },
        "Docker-Run": {
            "Docker-Run": 1,
            "Demo-Advanced-Docker-Run-Features": 2,
        },
        "Docker-Compose": {
            "Docker-Compose": 1,
            "Demo-Docker-Compose": 2,
            "Demo-Example-Voting-Application": 3,
            "Demo-Example-Voting-Application-with-Docker-Compose": 4,
        },
        "Docker-Engine-Storage": {
            "Docker-Engine": 1,
            "Docker-Storage": 2,
        },
        "Docker-Registry": {
            "Docker-Registry": 1,
        },
        "Docker-on-Mac-Windows": {
            "Docker-on-Mac": 1,
            "Docker-on-Windows": 2,
        },
        "Container-Orchestration-Docker-Swarm-Kubernetes": {
            "Container-Orchestration": 1,
            "Docker-Swarm": 2,
            "Kubernetes-Introduction": 3,
        },
        "Twelve-Factor-App-methodology": {
            "Codebase": 1,
            "Dependencies": 2,
            "Config": 3,
            "Backing-Services": 4,
            "Build-Release-and-Run": 5,
            "Processes": 6,
            "Port-Binding": 7,
            "Concurrency": 8,
            "Disposability": 9,
            "Dev-Prod-Parity": 10,
            "Logs": 11,
            "Admin-Processes": 12,
        },
        "Introduction-to-Helm": {
            "What-is-Helm": 1,
            "A-quick-note-about-Helm2-vs-Helm3": 2,
            "Installation-and-configuration": 3,
            "Helm-Components": 4,
            "Helm-charts": 5,
            "Customizing-chart-parameters": 6,
            "Working-with-Helm-basics": 7,
            "Lifecycle-management-with-Helm": 8,
        },
        "Helm-Charts-Anatomy": {
            "Understanding-Helm-charts": 1,
            "Writing-a-Helm-chart": 2,
            "Customizing-chart-parameters": 3,  # might not be here
            "Named-Templates": 3,
            "Functions": 4,
            "Pipelines": 5,
            "Conditionals": 6,
            "With-Blocks": 7,
            "Ranges": 8,
            "Making-sure-Chart-is-working-as-intended": 9,
            "Packaging-and-Signing-Charts": 10,
            "Uploading-Charts": 11,
            "Chart-Hooks": 12,
        },
        "Communication-Expression-and-Storytelling": {
            "Communication-Expression-and-Storytelling": 1,
        },
        "Leading-with-Impact": {
            "Leading-with-Impact": 1,
        },
        "Fostering-Team-Alignment-and-Energy": {
            "Fostering-Team-Alignment-and-Energy": 1,
        },
        "Navigating-Priorities-and-Tasks": {
            "Navigating-Priorities-and-Tasks": 1,
        },
        "Embracing-Continuous-Evolution": {
            "Embracing-Continuous-Evolution": 1,
        },
        "Managing-Clients-and-Stakeholders": {
            "Managing-Clients-and-Stakeholders": 1,
        },
    }
    
    # Check module-specific lesson order
    if module_name in lesson_orders:
        return lesson_orders[module_name].get(lesson_name, 999)
    
    # Default: try to extract number from lesson name
    match = re.match(r'(\d+)', lesson_name)
    if match:
        return int(match.group(1))
    return 999


def fix_image_paths(content, course_dir):
    """Fix image paths in markdown content to be relative to the course directory."""
    # Pattern: ![alt](<relative-path-to-images-dir>/image.jpg)
    # The current paths are like: ../../../../images/kodekloud.com/...
    # We need to make them relative to the markdown file location
    
    def replace_image(match):
        alt = match.group(1)
        path = match.group(2)
        
        # If it's already a web URL, keep as is
        if path.startswith('http://') or path.startswith('https://'):
            return match.group(0)
        
        # If it's a local path, make sure it points to the right place
        # The images are stored in /opt/data/kodekloud-notes/repo/images/
        # The markdown files are in /opt/data/kodekloud-notes/repo/docs/Course/Module/Lesson/
        # So we need ../../../../images/... from the markdown file
        # But the current paths already use ../../../../images/... which should work
        
        # Check if the image file actually exists
        full_path = REPO_ROOT / path.lstrip('../../../../')
        if full_path.exists():
            # Path is correct, keep it
            return match.group(0)
        else:
            # Try to find the image by basename
            img_name = Path(path).name
            # Search in images directory
            for root, dirs, files in os.walk(IMAGES_DIR):
                if img_name in files:
                    found_path = Path(root) / img_name
                    rel_path = found_path.relative_to(REPO_ROOT)
                    new_path = f"../../../../{rel_path}"
                    return f"![{alt}]({new_path})"
            
            # If not found, keep original (will be broken but we tried)
            return match.group(0)
    
    # Replace all image references
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, content)
    return content


def fix_callout_syntax(content):
    """Fix Callout and other custom component syntax for better markdown rendering."""
    # Convert <Callout> to markdown blockquote with emoji
    content = re.sub(
        r'<Callout\s+icon="([^"]+)">\s*(.*?)\s*</Callout>',
        lambda m: f"> **{m.group(1)}** {m.group(2).strip()}",
        content,
        flags=re.DOTALL
    )
    
    # Convert <Frame> to markdown image with caption
    content = re.sub(
        r'<Frame>\s*!\[([^\]]*)\]\(([^)]+)\)\s*</Frame>',
        lambda m: f"![{m.group(1)}]({m.group(2)})",
        content,
        flags=re.DOTALL
    )
    
    # Convert <CardGroup><Card ... /></CardGroup> to simple links
    content = re.sub(
        r'<CardGroup>\s*(.*?)\s*</CardGroup>',
        lambda m: re.sub(r'<Card\s+title="([^"]+)"\s+icon="[^"]+"\s+href="([^"]+)"\s*/>', r'- [\1](\2)', m.group(1)),
        content,
        flags=re.DOTALL
    )
    
    return content


def process_course(course_dir):
    """Process a single course directory to fix ordering and images."""
    course_name = course_dir.name
    print(f"\nProcessing course: {course_name}")
    
    # Get all module directories
    modules = [d for d in course_dir.iterdir() if d.is_dir()]
    
    # Sort modules by correct order
    modules_sorted = sorted(modules, key=lambda m: get_module_order(course_name, m.name.split('-', 1)[1] if '-' in m.name else m.name))
    
    # Rename directories with correct prefix
    for i, module_dir in enumerate(modules_sorted, 1):
        old_name = module_dir.name
        # Extract module name without existing prefix
        module_name = old_name.split('-', 1)[1] if '-' in old_name else old_name
        new_name = f"{i:02d}-{module_name}"
        
        if old_name != new_name:
            new_path = module_dir.parent / new_name
            print(f"  Renaming module: {old_name} -> {new_name}")
            module_dir.rename(new_path)
            module_dir = new_path
        
        # Process lessons within module
        lessons = [d for d in module_dir.iterdir() if d.is_dir()]
        lessons_sorted = sorted(lessons, key=lambda l: get_lesson_order(course_name, module_name, l.name.split('-', 1)[1] if '-' in l.name else l.name))
        
        for j, lesson_dir in enumerate(lessons_sorted, 1):
            old_lesson_name = lesson_dir.name
            lesson_name = old_lesson_name.split('-', 1)[1] if '-' in old_lesson_name else old_lesson_name
            new_lesson_name = f"{j:02d}-{lesson_name}"
            
            if old_lesson_name != new_lesson_name:
                new_lesson_path = lesson_dir.parent / new_lesson_name
                print(f"    Renaming lesson: {old_lesson_name} -> {new_lesson_name}")
                lesson_dir.rename(new_lesson_path)
                lesson_dir = new_lesson_path
            
            # Fix markdown content in lesson
            md_files = list(lesson_dir.glob("*.md"))
            for md_file in md_files:
                content = md_file.read_text(encoding='utf-8')
                original_content = content
                
                # Fix image paths
                content = fix_image_paths(content, course_dir)
                
                # Fix callout/frame/card syntax
                content = fix_callout_syntax(content)
                
                if content != original_content:
                    md_file.write_text(content, encoding='utf-8')
                    print(f"      Fixed content in: {md_file.relative_to(REPO_ROOT)}")


def main():
    print("Starting KodeKloud notes fix...")
    
    # Process each course
    for course_dir in sorted(DOCS_DIR.iterdir()):
        if course_dir.is_dir():
            # Only process known courses for now
            if course_dir.name in COURSE_MODULE_ORDER:
                process_course(course_dir)
            else:
                print(f"Skipping unknown course: {course_dir.name}")
    
    print("\nDone!")


if __name__ == "__main__":
    main()