# scripts

Operational notes for repository helper scripts.

## `count_text_size.py`

Count `chars`, `words`, and `lines` for one or more files, with optional Markdown heading breakdown.

Examples:

```bash
python3 scripts/count_text_size.py README.md
python3 scripts/count_text_size.py skills/software-design-doc/SKILL.md --by-heading
python3 scripts/count_text_size.py --format json README.md
python3 scripts/count_text_size.py --version
```

Skill-local duplicate:

```bash
python3 skills/software-design-doc/scripts/count_text_size.py --version
```

## `sync_duplicated_scripts.py`

Synchronize intentionally duplicated script copies from canonical source paths.

Examples:

```bash
python3 scripts/sync_duplicated_scripts.py
python3 scripts/sync_duplicated_scripts.py --check
python3 scripts/sync_duplicated_scripts.py --check --verify-hash
```

Current mapping:

- `scripts/count_text_size.py` -> `skills/software-design-doc/scripts/count_text_size.py`

Maintenance:

- Keep duplicated copies byte-identical.
- When the duplicated script changes, update `Version` and `Synced-On` headers in both copies.
