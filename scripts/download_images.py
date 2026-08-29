#!/usr/bin/env python3
"""
Download all images from KodeKloud website by scraping course pages.
Matches images by alt text and downloads to local images directory.
"""
import os
import re
import requests
from pathlib import Path

REPO_DOCS = Path("/opt/data/kodekloud-notes/repo/docs")
REPO_IMAGES = Path("/opt/data/kodekloud-notes/repo/images")
OUTPUT_DIR = Path("/opt/data/kodekloud-notes/repo")

def download_course_images(course_name):
    """Download all images for a course from the website."""
    print(f"Processing {course_name}...")
    
    url = f"https://notes.kodekloud.com/docs/{course_name}/"
    resp = requests.get(url, timeout=30)
    if resp.status_code != 200:
        print(f"  Failed to fetch course page: {resp.status_code}")
        return
    
    # Get all module/lesson URLs
    lesson_urls = []
    for match in re.finditer(r'href="/docs/[^/]+/[^/]+/([^/]+)/', resp.text):
        module = match.group(1)
        # Need to get lessons for each module
        module_url = f"https://notes.kodekloud.com/docs/{course_name}/{module}/"
        lesson_urls.append(module_url)
    
    # Deduplicate
    lesson_urls = list(set(lesson_urls))
    print(f"  Found {len(lesson_urls)} module pages")
    
    # For each module page, get lesson pages
    all_lesson_urls = []
    for module_url in lesson_urls[:5]:  # Limit for testing
        module_resp = requests.get(module_url, timeout=30)
        if module_resp.status_code == 200:
            for match in re.finditer(r'href="/docs/[^/]+/[^/]+/([^/]+)/', module_resp.text):
                lesson = match.group(1)
                lesson_url = f"https://notes.kodekloud.com/docs/{course_name}/{module_url.split('/')[-2]}/{lesson}/"
                all_lesson_urls.append(lesson_url)
    
    # Deduplicate
    all_lesson_urls = list(set(all_lesson_urls))
    print(f"  Found {len(all_lesson_urls)} lesson pages")
    
    # Download images from each lesson page
    downloaded = 0
    for lesson_url in all_lesson_urls[:10]:  # Limit for testing
        lesson_resp = requests.get(lesson_url, timeout=30)
        if lesson_resp.status_code == 200:
            # Extract images with data-path and alt
            for match in re.finditer(r'<img\s+data-path="([^"]+)"\s+src="[^"]+"\s+alt="([^"]+)"', lesson_resp.text):
                data_path = match.group(1)
                alt = match.group(2)
                
                full_path = OUTPUT_DIR / data_path
                if full_path.exists():
                    continue
                
                # Extract src from the same img tag
                # Find the complete img tag
                img_start = lesson_resp.text.find(data_path)
                if img_start > 0:
                    # Look for src in nearby text
                    context = lesson_resp.text[img_start-200:img_start+500]
                    src_match = re.search(r'src="([^"]+)"', context)
                    if src_match:
                        src = src_match.group(1)
                        os.makedirs(full_path.parent, exist_ok=True)
                        img_resp = requests.get(src, timeout=30)
                        if img_resp.status_code == 200:
                            with open(full_path, 'wb') as f:
                                f.write(img_resp.content)
                            downloaded += 1
                            print(f"    Downloaded: {data_path}")
    
    print(f"  Downloaded {downloaded} new images")

def main():
    courses = sorted([d for d in os.listdir(REPO_DOCS) if os.path.isdir(REPO_DOCS / d)])
    print(f"Total courses: {len(courses)}")
    
    # Process a few courses for testing
    for course in courses[:3]:
        download_course_images(course)

if __name__ == "__main__":
    main()