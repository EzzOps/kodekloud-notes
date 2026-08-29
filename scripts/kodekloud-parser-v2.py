#!/usr/bin/env python3
"""
Complete KodeKloud Notes Parser with Correct Ordering
- Downloads llms-full.txt and llms.txt
- Extracts correct module/lesson ordering from llms.txt (live website)
- Creates directory structure with proper numeric prefixes (01-, 02-, etc.)
- Fixes image paths to be relative and valid
- Converts KodeKloud React components to standard Markdown
"""

import re
import requests
import json
import os
import shutil
from pathlib import Path
from collections import OrderedDict

LLMS_FULL_URL = "https://notes.kodekloud.com/llms-full.txt"
LLMS_TXT_URL = "https://notes.kodekloud.com/llms.txt"
OUTPUT_DIR = Path("/opt/data/kodekloud-notes/repo")
DOCS_DIR = OUTPUT_DIR / "docs"
IMAGES_DIR = OUTPUT_DIR / "images"


def download_llms_full():
    """Download the full concatenated content file."""
    print(f"Downloading {LLMS_FULL_URL}...")
    resp = requests.get(LLMS_FULL_URL, timeout=120)
    resp.raise_for_status()
    print(f"Downloaded {len(resp.text):,} chars ({len(resp.text)/(1024*1024):.1f} MB)")
    return resp.text


def download_llms_txt():
    """Download the llms.txt index file for correct ordering."""
    print(f"Downloading {LLMS_TXT_URL}...")
    resp = requests.get(LLMS_TXT_URL, timeout=60)
    resp.raise_for_status()
    print(f"Downloaded {len(resp.text):,} chars")
    return resp.text


def load_merged_ordering():
    """Load merged ordering from scraped data + llms.txt + llms-full.txt for all 180 courses."""
    ordering_file = OUTPUT_DIR / "course_ordering_final.json"
    if ordering_file.exists():
        with open(ordering_file) as f:
            data = json.load(f)
        print(f"Loaded final ordering for {len(data['course_modules'])} courses")
        return data['course_modules'], {tuple(k.split('|')): v for k, v in data['course_lessons'].items()}
    else:
        # Fallback
        return load_fallback_ordering()


def load_fallback_ordering():
    """Load fallback ordering from scraped + llms.txt."""
    ordering_file = OUTPUT_DIR / "course_ordering_merged.json"
    if ordering_file.exists():
        with open(ordering_file) as f:
            data = json.load(f)
        print(f"Loaded fallback ordering for {len(data['course_modules'])} courses")
        return data['course_modules'], {tuple(k.split('|')): v for k, v in data['course_lessons'].items()}
    else:
        # Last resort: llms.txt only
        return extract_ordering_from_llms_txt(download_llms_txt())


def extract_ordering_from_llms_txt(content):
    """Extract correct module/lesson ordering from llms.txt."""
    # Pattern: - [Title](https://notes.kodekloud.com/docs/Course/Module/Lesson/page.md)
    pattern = r'- \[([^\]]+)\]\(https://notes\.kodekloud\.com/docs/([^/]+)/([^/]+)/([^/]+)/page\.md\)'
    
    course_modules = OrderedDict()
    course_lessons = OrderedDict()
    
    for match in re.finditer(pattern, content):
        title = match.group(1)
        course = match.group(2)
        module = match.group(3)
        lesson = match.group(4)
        
        # Track module order per course
        if course not in course_modules:
            course_modules[course] = []
        if module not in course_modules[course]:
            course_modules[course].append(module)
        
        # Track lesson order per module
        key = (course, module)
        if key not in course_lessons:
            course_lessons[key] = []
        if lesson not in course_lessons[key]:
            course_lessons[key].append(lesson)
    
    print(f"Extracted ordering for {len(course_modules)} courses from llms.txt")
    return course_modules, course_lessons


def parse_and_split(content):
    """Split llms-full.txt by source URLs into individual files."""
    pattern = r'^# (.+?)\nSource: (https://notes\.kodekloud\.com/docs/.+?/page)\n\n(.*?)(?=\n^# |\Z)'
    matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
    
    pages = []
    for m in matches:
        title = m.group(1)
        url = m.group(2)
        body = m.group(3).strip()
        pages.append((title, url, body))
    
    return pages


def fix_image_paths(content, md_file_path):
    """Fix image paths in markdown content to be relative to the markdown file."""
    # The markdown file will be at docs/Course/Module/Lesson/page.md
    # Images are at images/kodekloud.com/...
    # Relative path from lesson dir: ../../../../images/...
    
    def replace_image(match):
        alt = match.group(1)
        path = match.group(2)
        
        # If it's already a web URL, keep as is
        if path.startswith('http://') or path.startswith('https://'):
            return match.group(0)
        
        # If it's already a relative path starting with ../../../../images/
        if path.startswith('../../../../images/'):
            # Verify the image exists
            rel_path = path[len('../../../../'):]
            full_path = OUTPUT_DIR / rel_path
            if full_path.exists():
                return match.group(0)
            # Try to find by basename
            img_name = Path(path).name
            for root, dirs, files in os.walk(IMAGES_DIR):
                if img_name in files:
                    found_path = Path(root) / img_name
                    rel_found = found_path.relative_to(OUTPUT_DIR)
                    new_path = f"../../../../{rel_found}"
                    return f"![{alt}]({new_path})"
            return match.group(0)
        
        # If it's some other relative path, try to find the image
        img_name = Path(path).name
        for root, dirs, files in os.walk(IMAGES_DIR):
            if img_name in files:
                found_path = Path(root) / img_name
                rel_found = found_path.relative_to(OUTPUT_DIR)
                new_path = f"../../../../{rel_found}"
                return f"![{alt}]({new_path})"
        
        return match.group(0)
    
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


def url_to_course_module_lesson(url):
    """Extract course, module, lesson from URL."""
    # URL: https://notes.kodekloud.com/docs/Course/Module/Lesson/page
    path = url.replace('https://notes.kodekloud.com/', '')
    parts = path.split('/')
    if len(parts) >= 5:
        return parts[1], parts[2], parts[3]  # course, module, lesson
    return None, None, None


def save_pages_with_ordering(pages, course_modules, course_lessons):
    """Save parsed pages with correct numeric prefixes for ordering."""
    print(f"Saving {len(pages)} pages with correct ordering...")
    
    # Track created directories to avoid duplicates
    created_dirs = set()
    
    for i, (title, url, body) in enumerate(pages, 1):
        course, module, lesson = url_to_course_module_lesson(url)
        if not course:
            continue
        
        # Get correct order indices
        module_order = 1
        if course in course_modules and module in course_modules[course]:
            module_order = course_modules[course].index(module) + 1
        
        lesson_order = 1
        key = (course, module)
        if key in course_lessons and lesson in course_lessons[key]:
            lesson_order = course_lessons[key].index(lesson) + 1
        
        # Build paths with numeric prefixes
        module_dir_name = f"{module_order:02d}-{module}"
        lesson_dir_name = f"{lesson_order:02d}-{lesson}"
        
        # Create directory structure
        module_dir = DOCS_DIR / course / module_dir_name
        lesson_dir = module_dir / lesson_dir_name
        lesson_dir.mkdir(parents=True, exist_ok=True)
        
        # Write markdown file
        md_file = lesson_dir / "page.md"
        
        # Fix content
        content = f"# {title}\n\nSource: {url}\n\n{body}\n"
        content = fix_callout_syntax(content)
        content = fix_image_paths(content, md_file)
        
        md_file.write_text(content, encoding='utf-8')
        
        if i % 500 == 0:
            print(f"  {i}/{len(pages)} saved...")
    
    print(f"Done! {len(pages)} pages saved to {OUTPUT_DIR}")


def main():
    print("=" * 60)
    print("KodeKloud Notes Parser - Full Rebuild with Correct Ordering")
    print("=" * 60)
    
    # Clean output directory (except images and .git)
    if DOCS_DIR.exists():
        print(f"Cleaning {DOCS_DIR}...")
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Download llms-full.txt
    llms_full = download_llms_full()
    
    # Load merged ordering (scraped + llms.txt)
    course_modules, course_lessons = load_merged_ordering()
    
    # Parse and save pages with correct ordering
    pages = parse_and_split(llms_full)
    save_pages_with_ordering(pages, course_modules, course_lessons)
    
    # Stats
    courses = set()
    for _, url, _ in pages:
        course, _, _ = url_to_course_module_lesson(url)
        if course:
            courses.add(course)
    
    print(f"\nSummary:")
    print(f"  {len(pages)} pages")
    print(f"  {len(courses)} courses")


if __name__ == "__main__":
    main()