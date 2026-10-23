# trafa-api

A ChatGPT/Codex skill for working with the open Trafikanalys API at `api.trafa.se`.

It provides workflow instructions, product and variable metadata, documented API combinations, an OpenAPI contract, a Python client, and offline checks. It is independent of the separate `trafapy` repository.

## Repository layout

The repository root is the complete skill folder. `SKILL.md` is the entry point; `references/`, `scripts/`, `evaluation/`, `assets/`, and `agents/` contain the supporting files. Browse or download individual files directly from GitHub.

For a local filesystem installation, clone this repository into a directory named `trafa-api`. If your ChatGPT upload flow requires a ZIP, package the repository contents inside one top-level folder named `trafa-api` and preserve the directory structure.

## Install in ChatGPT

In a ChatGPT workspace that supports Skills and file uploads:

1. Open **Plugins → Skills → Create → Upload from your computer**.
2. Upload the ZIP package containing the `trafa-api` folder.
3. Review the skill and install it.
4. Start a new chat and invoke it with `@trafa-api`, or ask a relevant Trafikanalys API question.

Availability depends on the workspace plan, settings, and administrator permissions.

## Install in Codex

Clone the repository into the supported local skills directory, for example `~/.agents/skills/trafa-api`. Keep `SKILL.md`, `references/`, `scripts/`, `assets/`, `evaluation/`, and `agents/` together. Restart Codex if the skill does not appear.

## Trafikanalys statistics terms

Trafikanalys' rules for reusing its statistics and using the Statistics Portal are summarized in [DATA-TERMS.md](DATA-TERMS.md). Those terms apply to Trafikanalys data and website material; they do not license the code or other files in this repository.

## Scope and review

The skill guides queries to Trafikanalys' public statistics API. It does not provide a hosted MCP server or create an API connection by itself. Review its scripts and references before use, especially when adapting it to a managed workplace.

This repository has no separate open-source license for its code. Rights to third-party data and materials remain with their respective rights holders.
