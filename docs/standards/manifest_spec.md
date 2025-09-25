# MANIFEST.csv Specification

Columns:
- `path` — relative file path
- `sha256` — checksum
- `bytes` — file size
- `content_type` — e.g., text/markdown, application/pdf
- `version_tag` — e.g., v1.0.0
- `generated_at` — ISO timestamp

Use `scripts/build_manifest.py --update` to refresh.
