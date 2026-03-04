# Agent Software Doc Skills

**A collection of agent skills** for drafting, reviewing, and improving software documentation, aligned with the [Agent Skills open specification](https://agentskills.io/specification).

## Table of Contents


- [Agent Software Doc Skills](#agent-software-doc-skills)
  - [Table of Contents](#table-of-contents)
  - [Available Skills](#available-skills)
  - [Standards and Copyright Notice](#standards-and-copyright-notice)
  - [Quick Start](#quick-start)
  - [Install Specific Skill](#install-specific-skill)
    - [Copy-Paste Installation](#copy-paste-installation)


## Available Skills

| Skill | Description |
| ----- | ----------- |
| [software-design-doc](skills/software-design-doc) | Draft, review, and update **Software Design Documents (SDD)** with an **IEEE 1016-2009-inspired** pragmatic structure.† |

† See [Standards and Copyright Notice](#standards-and-copyright-notice).

## Standards and Copyright Notice

- This repository provides independently authored templates, checklists, and workflows informed by IEEE 1016-2009 concepts.
- It does not include IEEE standard text, figures, or tables, and it is not a substitute for the official standard.
- This repository is unofficial guidance.
- IEEE standards are copyrighted by IEEE; use a properly licensed copy when you need normative wording.
- "IEEE" and related marks are trademarks of IEEE.
- Official IEEE standard page: [IEEE Std 1016-2009](https://standards.ieee.org/ieee/1016/4502/).
- See [NOTICE](NOTICE) for the third-party standards notice included in this repository.

## Quick Start

To install all skills, use the following command:

- Install with [skills](https://github.com/vercel-labs/skills) CLI (recommended):

```bash
npx skills add https://github.com/RJTPP/agent-software-doc-skills --skill '*'  
```

- Install with **OpenAI Codex** via `$skill-installer` skill:

```md
$skill-installer install all skills from RJTPP/agent-software-doc-skills
```

## Install Specific Skill

To install a specific skill, replace the `<SKILL_NAME>` in the following command with the name of the skill you want to install:

- For Skills CLI:
```bash
npx skills add https://github.com/RJTPP/agent-software-doc-skills --skill <SKILL_NAME>
```

- For OpenAI Codex:
```md
$skill-installer install <SKILL_NAME> from RJTPP/agent-software-doc-skills
```

### Copy-Paste Installation

- [`software-design-doc`](skills/software-design-doc/):

```bash
npx skills add https://github.com/RJTPP/agent-software-doc-skills --skill software-design-doc
```
