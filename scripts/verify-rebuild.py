#!/usr/bin/env python3
"""Verify the rebuild was successful."""
import os
import re
import json

with open('course_ordering_final.json') as f:
    ordering = json.load(f)

repo_docs = 'docs'
images_dir = 'images'

def extract_name(d):
    return d.split('-', 1)[1] if '-' in d else d

all_ok = True
total_courses = 0
total_modules = 0
total_lessons = 0
total_images = 0
total_broken_images = 0
failures = []

for course_name in sorted(ordering['course_modules'].keys()):
    modules_data = {m: ordering['course_lessons'].get(f'{course_name}|{m}', []) for m in ordering['course_modules'][course_name]}
    course_path = os.path.join(repo_docs, course_name)
    if not os.path.exists(course_path):
        continue
    
    total_courses += 1
    expected_modules = list(modules_data.keys())
    actual_modules = [extract_name(d) for d in sorted(os.listdir(course_path)) if os.path.isdir(os.path.join(course_path, d))]
    total_modules += len(actual_modules)
    
    if expected_modules != actual_modules:
        failures.append(f"{course_name}: Module order mismatch")
        all_ok = False
        continue
    
    module_ok = True
    for module_name, expected_lessons in modules_data.items():
        module_idx = expected_modules.index(module_name) + 1
        module_path = os.path.join(course_path, f"{module_idx:02d}-{module_name}")
        if not os.path.exists(module_path):
            module_ok = False
            all_ok = False
            continue
        
        actual_lessons = [extract_name(d) for d in sorted(os.listdir(module_path)) if os.path.isdir(os.path.join(module_path, d))]
        total_lessons += len(actual_lessons)
        
        if expected_lessons != actual_lessons:
            failures.append(f"  {course_name}/{module_name}: Lesson order mismatch")
            module_ok = False
            all_ok = False

# Check images across all courses
for course_name in sorted(ordering['course_modules'].keys()):
    course_path = os.path.join(repo_docs, course_name)
    if not os.path.exists(course_path):
        continue
    
    for root, dirs, files in os.walk(course_path):
        for f in files:
            if f.endswith('.md'):
                md_path = os.path.join(root, f)
                with open(md_path, 'r', encoding='utf-8') as mf:
                    content = mf.read()
                
                for img_match in re.finditer(r'!\[([^\]]*)\]\(([^)]+)\)', content):
                    img_path = img_match.group(2)
                    total_images += 1
                    
                    if img_path.startswith('http://') or img_path.startswith('https://'):
                        continue
                    
                    if img_path.startswith('../../../../'):
                        rel_path = img_path[len('../../../../'):]
                        full_path = os.path.join(".", rel_path)
                    else:
                        img_name = os.path.basename(img_path)
                        found = False
                        for img_root, img_dirs, img_files in os.walk(images_dir):
                            if img_name in img_files:
                                found = True
                                full_path = os.path.join(img_root, img_name)
                                break
                        if not found:
                            total_broken_images += 1
                            all_ok = False
                            continue
                    
                    if not os.path.exists(full_path):
                        total_broken_images += 1
                        all_ok = False

print(f"Courses tested: {total_courses}")
print(f"Modules verified: {total_modules}")
print(f"Lessons verified: {total_lessons}")
print(f"Images checked: {total_images}")
print(f"Broken/missing images: {total_broken_images}")
print(f"Ordering failures: {len(failures)}")
if failures:
    for f in failures:
        print(f"  {f}")

print("=" * 70)
if all_ok:
    print("✅ ALL TESTS PASSED!")
else:
    print("❌ SOME TESTS FAILED")

exit(0 if all_ok else 1)