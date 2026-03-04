# software-design-doc

Operational notes for the `software-design-doc` skill and related helper scripts.

## Scripts

- Structure validator:

```bash
python3 skills/software-design-doc/scripts/check_sdd_structure.py --help
```

- Text size utility (skill-local copy):

```bash
python3 skills/software-design-doc/scripts/count_text_size.py SKILL.md --by-heading
python3 skills/software-design-doc/scripts/count_text_size.py --version
```

## Duplicated Script Sync

`count_text_size.py` is intentionally duplicated:

- Canonical source: `scripts/count_text_size.py`
- Skill-local copy: `skills/software-design-doc/scripts/count_text_size.py`

Sync and check with:

```bash
python3 scripts/sync_duplicated_scripts.py
python3 scripts/sync_duplicated_scripts.py --check --verify-hash
```

If either copy changes, update both header fields (`Version`, `Synced-On`) and re-run the sync check.
