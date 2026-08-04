# W08 Plan — ChatGPT Skills / Project Dual Deployment

## Objective
Provide a native-skill path when available and a ChatGPT Project + GitHub path otherwise,
without duplicating skill sources.

## Outputs
- deployment documentation
- PowerShell installer/updater
- release manifest and consumer lock format
- install validation workflow
- W08 result/state updates

## Gate
A consumer can pin a revision, install/update idempotently, verify hashes, and route to the
same skills under either deployment path. No unpinned remote execution is permitted.
