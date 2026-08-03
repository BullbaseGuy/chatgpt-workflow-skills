# Deployment Paths

This repository supports two deployment paths from the same source manifest.

| Path | Use when | Source of truth |
|---|---|---|
| Native ChatGPT Skills | The ChatGPT Skills upload/editor surface is available | Upload-ready folders generated from `release/skills-manifest.json` |
| ChatGPT Project + GitHub | Work is repository-centric or native Skills are unavailable | Connected GitHub repository plus project instructions pointing to the router and canonical task state |

Both paths use the same ten `SKILL.md` sources. Generated native bundles are build artifacts, not independently maintained copies. Consumer repositories pin an immutable 40-character commit in `.devflow/workflow-skills.lock.json` or the installed `.workflow-skills.lock.json`.

## Security invariant

The installer never executes downloaded content. It downloads the pinned manifest and its listed files, verifies every Git blob identity, stages the complete bundle, and only then atomically replaces the previous installation.

See:

- `NATIVE_CHATGPT_SKILLS.md`
- `CHATGPT_PROJECT_GITHUB.md`
- `CONSUMER_INSTALL.md`
