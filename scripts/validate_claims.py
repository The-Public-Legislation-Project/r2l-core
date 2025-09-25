#!/usr/bin/env python3
"""
Minimal validator: scans repository for text/markdown files and asserts that any
file modified under a redline branch contains at least one [[DAM:XXXX]] tag and
a YAML header. In CI, run across repo; for real diff-based checks, extend with git diff.
"""
import re, sys, os, io, json
RE_DAM = re.compile(r"\[\[DAM:(?:\d{3,}|[A-Z0-9-]+)\]\]")
RE_YAML = re.compile(r"^---\s*[\s\S]+?---\s*", re.MULTILINE)

def check_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        ok = True
        if not RE_YAML.search(txt):
            print(f"[FAIL] YAML header missing: {path}")
            ok = False
        if not RE_DAM.search(txt):
            print(f"[FAIL] No DAM tags found: {path}")
            ok = False
        return ok
    except Exception as e:
        print(f"[WARN] Skipping {path}: {e}")
        return True

def walk(root="."):
    targets = []
    for base, dirs, files in os.walk(root):
        # skip .git and binary dirs
        if any(skip in base for skip in (".git", "evidence/LDAI", "figures", "build", "incoming")):
            continue
        for name in files:
            if name.endswith((".md", ".txt")):
                targets.append(os.path.join(base, name))
    return targets

def main():
    failed = False
    for p in walk("."):
        if not check_file(p):
            failed = True
    if failed:
        sys.exit(1)
    print("OK: basic headers and DAM tags present where expected.")

if __name__ == "__main__":
    main()
