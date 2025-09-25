#!/usr/bin/env python3
"""
Builds or checks MANIFEST.csv: path, sha256, bytes, content_type, version_tag, generated_at
"""
import hashlib, os, csv, sys, time, mimetypes
from datetime import datetime

MANIFEST = "MANIFEST.csv"
VERSION = os.environ.get("R2L_TAG", "v0.0.0-dirty")

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def iter_files(root="."):
    for base, dirs, files in os.walk(root):
        if ".git" in base or "/incoming" in base:
            continue
        for name in files:
            p = os.path.join(base, name)
            yield p

def update():
    rows = []
    for p in iter_files("."):
        if os.path.basename(p) == "MANIFEST.csv":
            continue
        stat = os.stat(p)
        sha = sha256_file(p)
        ct, _ = mimetypes.guess_type(p)
        rows.append([p, sha, stat.st_size, ct or "application/octet-stream", VERSION, datetime.utcnow().isoformat() + "Z"])
    with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["path","sha256","bytes","content_type","version_tag","generated_at"])
        w.writerows(rows)
    print(f"Updated {MANIFEST} with {len(rows)} entries.")

def check():
    if not os.path.exists(MANIFEST):
        print("MANIFEST.csv missing")
        sys.exit(1)
    with open(MANIFEST, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = row["path"]
            if not os.path.exists(p):
                print(f"Missing file: {p}")
                sys.exit(1)
            if sha256_file(p) != row["sha256"]:
                print(f"Hash mismatch: {p}")
                sys.exit(1)
    print("Manifest OK.")

if __name__ == "__main__":
    mode = "--check" if "--check" in sys.argv else "--update"
    if mode == "--check":
        check()
    else:
        update()
