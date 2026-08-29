#!/usr/bin/env python3
"""
Fix KodeKloud course ordering and image paths for ALL courses.
- Reorder modules/lessons to match actual KodeKloud course sequence (from llms.txt scraping)
- Fix broken image paths to be relative/local
- Convert KodeKloud React components to standard Markdown
"""

import os
import re
import shutil
import json
from pathlib import Path
from collections import OrderedDict

REPO_ROOT = Path("/opt/data/kodekloud-notes/repo")
DOCS_DIR = REPO_ROOT / "docs"
IMAGES_DIR = REPO_ROOT / "images"

# Load course module order from scraped data
with open('/tmp/scraped_course_data_full.json') as f:
    SCRAPED_DATA = json.load(f)

# Build COURSE_MODULE_ORDER from scraped data
COURSE_MODULE_ORDER = {}
for course, modules in SCRAPED_DATA.items():
    COURSE_MODULE_ORDER[course] = {m: i+1 for i, m in enumerate(modules.keys())}

# Build LESSON_ORDER from scraped data
LESSON_ORDER = {}
for course, modules in SCRAPED_DATA.items():
    for module, lessons in modules.items():
        LESSON_ORDER[(course, module)] = {l: i+1 for i, l in enumerate(lessons)}


def get_module_order(course_name, module_name):
    """Get the correct order index for a module within a course."""
    if course_name in COURSE_MODULE_ORDER:
        return COURSE_MODULE_ORDER[course_name].get(module_name, 999)
    return 999


def get_lesson_order(course_name, module_name, lesson_name):
    """Get the correct order index for a lesson within a module."""
    key = (course_name, module_name)
    if key in LESSON_ORDER:
        return LESSON_ORDER[key].get(lesson_name, 999)
    # Default: try to extract number from lesson name
    match = re.match(r'(\d+)', lesson_name)
    if match:
        return int(match.group(1))
    return 999


def fix_image_paths(content, course_dir):
    """Fix image paths in markdown content to be relative to the course directory."""
    
    def replace_image(match):
        alt = match.group(1)
        path = match.group(2)
        
        # If it's already a web URL, keep as is
        if path.startswith('http://') or path.startswith('https://'):
            return match.group(0)
        
        # Check if the image file actually exists at the resolved path
        # The markdown file is at docs/Course/Module/Lesson/page.md
        # Image paths are like ../../../../images/...
        md_file_dir = Path(course_dir)  # This is a bit approximate
        
        # Try to resolve from the repo root
        if path.startswith('../../../../'):
            rel_path = path[len('../../../../'):]
            full_path = REPO_ROOT / rel_path
        else:
            # Try to find by basename
            img_name = Path(path).name
            for root, dirs, files in os.walk(IMAGES_DIR):
                if img_name in files:
                    found_path = Path(root) / img_name
                    rel_path = found_path.relative_to(REPO_ROOT)
                    new_path = f"../../../../{rel_path}"
                    return f"![{alt}]({new_path})"
            return match.group(0)
        
        if full_path.exists():
            return match.group(0)
        else:
            # Try to find by basename
            img_name = Path(path).name
            for root, dirs, files in os.walk(IMAGES_DIR):
                if img_name in files:
                    found_path = Path(root) / img_name
                    rel_path = found_path.relative_to(REPO_ROOT)
                    new_path = f"../../../../{rel_path}"
                    return f"![{alt}]({new_path})"
            return match.group(0)
    
    # Replace all image references
    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_image, content)
    return content


def fix_callout_syntax(content):
    """Fix Callout and other custom component syntax for better markdown rendering."""
    # Convert <Callout icon="lightbulb">content</Callout> to markdown blockquote with emoji
    content = re.sub(
        r'<Callout\s+icon="([^"]+)">\s*(.*?)\s*</Callout>',
        lambda m: f"> **{m.group(1)}** {m.group(2).strip()}",
        content,
        flags=re.DOTALL
    )
    
    # Convert <Frame>![alt](path)</Frame> to standard markdown image
    content = re.sub(
        r'<Frame>\s*!\[([^\]]*)\]\(([^)]+)\)\s*</Frame>',
        lambda m: f"![{m.group(1)}]({m.group(2)})",
        content,
        flags=re.DOTALL
    )
    
    # Convert <CardGroup><Card title="X" icon="Y" href="Z" /></CardGroup> to simple links
    content = re.sub(
        r'<CardGroup>\s*(.*?)\s*</CardGroup>',
        lambda m: re.sub(r'<Card\s+title="([^"]+)"\s+icon="[^"]+"\s+href="([^"]+)"\s*/>', r'- [\1](\2)', m.group(1)),
        content,
        flags=re.DOTALL
    )
    
    # Convert remaining <Card ... /> to links
    content = re.sub(
        r'<Card\s+title="([^"]+)"\s+icon="[^"]+"\s+href="([^"]+)"\s*/>',
        r'- [\1](\2)',
        content
    )
    
    return content


def extract_name(dir_name):
    """Extract the name part after the numeric prefix."""
    if '-' in dir_name:
        return dir_name.split('-', 1)[1]
    return dir_name


def process_course(course_dir):
    """Process a single course directory to fix ordering and images."""
    course_name = course_dir.name
    print(f"\nProcessing course: {course_name}")
    
    # Skip if not in scraped data
    if course_name not in COURSE_MODULE_ORDER:
        print(f"  Skipping: No ordering data available")
        return
    
    # Get all module directories
    modules = [d for d in course_dir.iterdir() if d.is_dir()]
    
    # Sort modules by correct order
    modules_sorted = sorted(modules, key=lambda m: get_module_order(course_name, extract_name(m.name)))
    
    # Rename directories with correct prefix
    for i, module_dir in enumerate(modules_sorted, 1):
        old_name = module_dir.name
        module_name = extract_name(old_name)
        new_name = f"{i:02d}-{module_name}"
        
        if old_name != new_name:
            new_path = module_dir.parent / new_name
            print(f"  Renaming module: {old_name} -> {new_name}")
            module_dir.rename(new_path)
            module_dir = new_path
        
        # Process lessons within module
        lessons = [d for d in module_dir.iterdir() if d.is_dir()]
        lessons_sorted = sorted(lessons, key=lambda l: get_lesson_order(course_name, module_name, extract_name(l.name)))
        
        for j, lesson_dir in enumerate(lessons_sorted, 1):
            old_lesson_name = lesson_dir.name
            lesson_name = extract_name(old_lesson_name)
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
    print("Starting KodeKloud notes fix for ALL courses...")
    print(f"Found {len(COURSE_MODULE_ORDER)} courses with ordering data")
    
    # Process each course that we have ordering data for
    for course_dir in sorted(DOCS_DIR.iterdir()):
        if course_dir.is_dir() and course_dir.name in COURSE_MODULE_ORDER:
            process_course(course_dir)
        elif course_dir.is_dir():
            print(f"Skipping unknown course: {course_dir.name}")
    
    print("\nDone!")


if __name__ == "__main__":
    main()