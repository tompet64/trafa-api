# trafa-api

A ChatGPT/Codex skill for working with the open Trafikanalys API at `api.trafa.se`.

It provides workflow instructions, product and variable metadata, documented API combinations, an OpenAPI contract, a Python client, and offline checks. It is independent of the separate `trafapy` repository.

## Package

The complete skill folder is distributed in [trafa-api-2026-10-19.zip](./trafa-api-2026-10-19.zip). Extract it as a folder named `trafa-api`; preserve its internal directory structure.

## Install in ChatGPT

In a ChatGPT workspace that supports Skills and file uploads:

1. Open **Plugins → Skills → Create → Upload from your computer**.
2. Upload the ZIP package.
3. Review the skill and install it.
4. Start a new chat and invoke it with `@trafa-api`, or ask a relevant Trafikanalys API question.

Availability depends on the workspace plan, settings, and administrator permissions.

## Install in Codex

Extract the ZIP and place the `trafa-api` directory in the supported local skills directory, for example `~/.agents/skills/trafa-api`. Keep `SKILL.md`, `references/`, `scripts/`, `assets/`, and `agents/` together. Restart Codex if the skill does not appear.

## Scope and review

The skill guides queries to Trafikanalys' public statistics API. It does not provide a hosted MCP server or create an API connection by itself. Review its scripts and references before use, especially when adapting it to a managed workplace.

No license file is included. All rights remain with their respective rights holders; this repository does not grant a general license for reuse or redistribution.
