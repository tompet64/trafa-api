# trafa-api

A ChatGPT/Codex skill for working with the open Trafikanalys API at `api.trafa.se`.

It provides workflow instructions, product and variable metadata, documented API combinations, an OpenAPI contract, a Python client, and offline checks. It is independent of the separate `trafapy` repository.

## AI disclosure

Most of this repository's original content—including its skill instructions, Python code, tests, and supporting documentation—was created with ChatGPT assistance, based on prompts and direction from the repository owner. Trafikanalys statistics and API-derived metadata are sourced separately; they are not ChatGPT-generated, and their reuse is governed by [DATA-TERMS.md](DATA-TERMS.md). AI-assisted content may contain errors: review the code and validate results before use. The licensed code is provided “as is” under the MIT License.

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

Trafikanalys' rules for reusing its statistics and using the Statistics Portal are summarized in [DATA-TERMS.md](DATA-TERMS.md). Those terms apply to Trafikanalys data and website material; they are separate from the license for this project's code.

## Code license

The original Python source files (`*.py`) under `scripts/` and `evaluation/` are licensed under the MIT License; see [LICENSE](LICENSE). This license covers only project code whose rights are controlled by the repository owner. It does not cover statistics returned by Trafikanalys' API, API-derived metadata, third-party material, or other files in this repository unless a file states otherwise. Check [DATA-TERMS.md](DATA-TERMS.md) and any source-specific notices for those materials.

The code is provided “as is”, without warranty, and users are responsible for its use and for validating its results.

## Scope and review

The skill guides queries to Trafikanalys' public statistics API. It does not provide a hosted MCP server or create an API connection by itself. Review its scripts and references before use, especially when adapting it to a managed workplace.
