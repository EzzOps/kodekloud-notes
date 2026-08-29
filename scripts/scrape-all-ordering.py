#!/usr/bin/env python3
"""
Scrape correct course module/lesson ordering from KodeKloud website for ALL courses.
Handles rate limiting with exponential backoff.
"""
import requests
import re
import os
import time
import json
from collections import OrderedDict
from pathlib import Path

REPO_DOCS = Path("/opt/data/kodekloud-notes/repo/docs")
OUTPUT_FILE = "/tmp/all_180_ordering_final.json"

def scrape_course(course, session, max_retries=5):
    """Scrape a single course's module/lesson ordering."""
    url = f"https://notes.kodekloud.com/docs/{course}/"
    
    for attempt in range(max_retries):
        try:
            resp = session.get(url, timeout=30)
            if resp.status_code == 200:
                modules = OrderedDict()
                # Pattern: /docs/Course/Module/Lesson/page or /docs/Course/Module/Lesson/page.md
                for match in re.finditer(r'href="/docs/[^/]+/([^/]+)/([^/]+)/', resp.text):
                    module = match.group(1)
                    lesson = match.group(2)
                    if module not in modules:
                        modules[module] = []
                    if lesson not in modules[module]:
                        modules[module].append(lesson)
                if modules:
                    return {m: lessons for m, lessons in modules.items()}
                return None
            elif resp.status_code == 404:
                return None
            elif resp.status_code == 403:
                # Rate limited - wait longer
                wait = (2 ** attempt) * 5
                print(f"  403 for {course}, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  HTTP {resp.status_code} for {course}")
                return None
        except Exception as e:
            print(f"  Error for {course}: {e}")
            time.sleep(2 ** attempt)
    
    return None

def main():
    courses_in_repo = sorted([d for d in os.listdir(REPO_DOCS) if os.path.isdir(REPO_DOCS / d)])
    print(f"Scraping {len(courses_in_repo)} courses...")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    all_data = {}
    success_count = 0
    fail_count = 0
    
    for i, course in enumerate(courses_in_repo):
        result = scrape_course(course, session)
        if result:
            all_data[course] = result
            success_count += 1
        else:
            fail_count += 1
        
        if i % 10 == 0:
            print(f"[{i+1}/{len(courses_in_repo)}] {course}: {'OK' if result else 'FAILED'} (success={success_count}, fail={fail_count})")
        
        # Be nice to the server
        time.sleep(0.2)
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(all_data, f, indent=2)
    
    print(f"\nScraped {success_count} courses successfully, {fail_count} failed")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()