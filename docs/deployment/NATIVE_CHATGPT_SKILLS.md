# Native ChatGPT Skills Deployment

OpenAI documents a ChatGPT Skills surface that can create, edit, share, install, and upload Skills. Uploaded Skills may include instructions, supporting files, and code, and should be reviewed before installation. Availability and administration can depend on account or workspace settings.

Official reference:
https://help.openai.com/en/articles/20001066-skills-in-chatgpt

## Build upload-ready folders

From a trusted checkout of an exact commit:

```powershell
$Out = Join-Path $env:TEMP 'bullbase-native-skills'
python scripts/build_native_skill_bundles.py --output $Out
```

The command creates one folder per skill. Each folder contains:

- `SKILL.md` at the bundle root;
- all referenced shared documents under `references/`;
- templates under `templates/`;
- the repository and upstream MIT license texts.

The duplication exists only in generated upload artifacts. Edit the source files in this repository, then rebuild; never edit generated bundles as a second source of truth.

## Install

1. Review `release/skills-manifest.json` and the generated folder.
2. In ChatGPT Skills, choose the create/upload path exposed by the current product UI.
3. Upload one generated skill folder.
4. Install `workflow-router` first; install downstream skills used by your workflow.
5. Run a routing smoke test with a task ID and verify it selects `durable-handoff` then `execution-supervisor` without asking for known context.

## Update

Rebuild from a newer reviewed commit and upload the replacement. Record the source commit in the skill description or deployment register so the installed version remains auditable.
