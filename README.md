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
  - [Future Plans](#future-plans)
    - [Skills](#skills)
    - [Intended Documentation Flow](#intended-documentation-flow)

## Available Skills

| Skill                                             | Description                                                                                                                |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| [software-design-doc](skills/software-design-doc) | Draft, review, and update **Software Design Descriptions (SDD)** with an **IEEE 1016-2009-inspired** pragmatic structure.† |

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

## Future Plans

The items below are exploratory roadmap candidates and may change in the future.

### Skills

| Skill                     | Description                                                                                                                                                                                                                             | Reference                                          |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| product-requirements-doc  | Elicit business goals from the user and produce a structured **Product Requirements Document (PRD)**.                                                                                                                                   | Industry practice (no formal IEEE standard)        |
| software-requirements-doc | Draft and review **Software Requirements Specifications (SRS/SRD)** with an IEEE 29148-2018-inspired structure.                                                                                                                         | IEEE 29148-2018                                    |
| readme-creator            | Create/update **README.md** from repository context, with optional related repository documentation consistency updates.                                                                                                                | Repository documentation best practices            |
| docs-composer             | Compose the full documentation suite by coordinating the available skills together end-to-end.                                                                                                                                          | —                                                  |
| docs-openspec-sync        | Bridge formal docs and [OpenSpec](https://github.com/Fission-AI/OpenSpec) tasks — convert SDD/SRD into OpenSpec change artifacts, or sync OpenSpec tasks back to docs. Detects if OpenSpec is installed and guides installation if not. | [OpenSpec](https://github.com/Fission-AI/OpenSpec) |

### Intended Documentation Flow

```text
PRD  →  SRD  →  SDD  ─────────────►  (implementation)  →  README.md
                  │                          ▲
                  └──►  OpenSpec tasks  ─────┘
                        (via docs-openspec-sync)
```

Each skill would handle one layer of the pipeline, from high-level business requirements through to a deployable, documented project.
