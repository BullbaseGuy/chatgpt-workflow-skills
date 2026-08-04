# Pinned Consumer Installation

## Install from an exact commit

```powershell
$Revision = '<40-character-reviewed-commit>'
pwsh -File .\scripts\install-workflow-skills.ps1 `
  -Revision $Revision `
  -Destination .\.agents\workflow-skills
```

For a local checked-out source, CI, or an air-gapped review:

```powershell
pwsh -File .\scripts\install-workflow-skills.ps1 `
  -Revision $Revision `
  -OfflineSourceRoot D:\src\chatgpt-workflow-skills `
  -Destination .\.agents\workflow-skills
```

The revision parameter rejects branch names and abbreviated SHAs. The installer:

1. loads `release/skills-manifest.json` from the same exact revision;
2. validates normalized source and destination paths;
3. downloads or reads only manifest-listed files;
4. recomputes each Git blob SHA;
5. stages and verifies the whole bundle;
6. atomically replaces the destination;
7. writes `.workflow-skills.lock.json`.

Running the same revision again returns `UNCHANGED` after verifying all installed hashes. A modified installed file is treated as tampering and fails verification rather than being silently accepted.

## Update

Review the new source diff and manifest, then rerun the command with the new full commit SHA. Do not point consumers at `main`, a tag that can move, or a remote script URL without a fixed commit.
