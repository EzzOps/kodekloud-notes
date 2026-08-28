#!/usr/bin/env python3
"""
Parse llms-full.txt and split into organized repo structure.
Bypasses Cloudflare 403 by using the pre-aggregated file.
"""
import re
import requests
from pathlib import Path

LLMS_FULL_URL = "https://notes.kodekloud.com/llms-full.txt"
OUTPUT_DIR = Path("/opt/data/kodekloud-notes/repo")

def download_llms_full():
    """Download the full concatenated content file."""
    print(f"Downloading {LLMS_FULL_URL}...")
    resp = requests.get(LLMS_FULL_URL, timeout=120)
    resp.raise_for_status()
    print(f"Downloaded {len(resp.text):,} chars ({len(resp.text)/(1024*1024):.1f} MB)")
    return resp.text

def parse_and_split(content):
    """Split llms-full.txt by source URLs into individual files."""
    # Pattern: # Title\nSource: https://notes.kodekloud.com/docs/.../page\n\nContent...
    pattern = r'^# (.+?)\nSource: (https://notes\.kodekloud\.com/docs/.+?/page)\n\n(.*?)(?=\n^# |\Z)'
    matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
    
    pages = []
    for m in matches:
        title = m.group(1)
        url = m.group(2)
        body = m.group(3).strip()
        pages.append((title, url, body))
    
    return pages

def url_to_path(url):
    """Convert source URL to local file path."""
    # Remove base URL prefix
    path = url.replace('https://notes.kodekloud.com/', '')
    # path is now 'docs/Course/Module/Topic/page'
    return OUTPUT_DIR / f"{path}.md"

def save_pages(pages):
    """Save parsed pages to organized directory structure."""
    print(f"Saving {len(pages)} pages...")
    for i, (title, url, body) in enumerate(pages, 1):
        out_path = url_to_path(url)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write markdown with title + content
        content = f"# {title}\n\nSource: {url}\n\n{body}\n"
        out_path.write_text(content, encoding='utf-8')
        
        if i % 500 == 0:
            print(f"  {i}/{len(pages)} saved...")
    
    print(f"Done! {len(pages)} pages in {OUTPUT_DIR}")

def main():
    content = download_llms_full()
    pages = parse_and_split(content)
    save_pages(pages)
    
    # Stats
    courses = set()
    for _, url, _ in pages:
        course = url.split('/')[4]  # Extract course name
        courses.add(course)
    
    print(f"\nSummary:")
    print(f"  {len(pages)} pages")
    print(f"  {len(courses)} courses")
    print(f"  Output: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
