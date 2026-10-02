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

## `check_doc_artifacts.py`

Check dated Markdown artifact history for a document kind. This checks existence,
filenames, and readability; content and current-run output must be checked separately.

```bash
python3 scripts/check_doc_artifacts.py --artifact-root .agent-doc-skills --doc-kind sdd --artifact-kind gaps
python3 scripts/check_doc_artifacts.py --artifact-root .agent-doc-skills --doc-kind adr --artifact-kind gaps
```

The canonical script is duplicated in the SDD and ADR skills so installed skills
remain self-contained. Sync and verify both destinations together:

```bash
python3 scripts/sync_duplicated_scripts.py --src scripts/check_doc_artifacts.py --dst skills/software-design-doc/scripts/check_doc_artifacts.py --dst skills/architecture-decision-record/scripts/check_doc_artifacts.py
python3 scripts/sync_duplicated_scripts.py --src scripts/check_doc_artifacts.py --dst skills/software-design-doc/scripts/check_doc_artifacts.py --dst skills/architecture-decision-record/scripts/check_doc_artifacts.py --check --verify-hash
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
