# scripts

Operational notes for repository helper scripts.

## `count_text_size.py`

Count `chars`, `words`, and `lines` for one or more files, with optional Markdown heading breakdown.

Examples:

```bash
python3 scripts/count_text_size.py README.md
python3 scripts/count_text_size.py skills/software-design-doc/SKILL.md --by-heading
python3 scripts/count_text_size.py --format json README.md
cat README.md | python3 scripts/count_text_size.py -
python3 scripts/count_text_size.py --glob "**/*.md"
python3 scripts/count_text_size.py --version
```

Skill-local duplicate:

```bash
python3 skills/software-design-doc/scripts/count_text_size.py --version
```

## `sync_duplicated_scripts.py`

Synchronize duplicated files from canonical source paths.

Examples:

```bash
# One-off explicit source/destination(s)
python3 scripts/sync_duplicated_scripts.py --src scripts/count_text_size.py --dst skills/software-design-doc/scripts/count_text_size.py

# One-off drift check
python3 scripts/sync_duplicated_scripts.py --src scripts/count_text_size.py --dst skills/software-design-doc/scripts/count_text_size.py --check --verify-hash
```

JSON map mode:

```bash
python3 scripts/sync_duplicated_scripts.py --map scripts/sync-map.json
python3 scripts/sync_duplicated_scripts.py --map scripts/sync-map.json --check
```

Map format (array or `{ "entries": [...] }`):

```json
[
  {
    "source": "scripts/count_text_size.py",
    "destinations": ["skills/software-design-doc/scripts/count_text_size.py"]
  }
]
```

Maintenance:

- Keep duplicated copies byte-identical.
- When the duplicated script changes, update `Version` and `Synced-On` headers in both copies.
