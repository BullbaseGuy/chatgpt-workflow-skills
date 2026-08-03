# PowerShell Manual Wizard Manifest Schema

## Required shape

```json
{
  "schema_version": "1.0.0",
  "title": "Configure example integration",
  "repository": "owner/repo",
  "stages": []
}
```

Stage IDs are unique and execute in listed order.

## Stage types

### `open_url`

```json
{
  "id": "open-settings",
  "title": "Open repository settings",
  "type": "open_url",
  "url": "https://github.com/owner/repo/settings/secrets/actions"
}
```

The URL must be a reviewed `http` or `https` URI. Private endpoints must not be committed.

### `capture`

```json
{
  "id": "capture-key",
  "title": "Capture service key",
  "type": "capture",
  "name": "SERVICE_API_KEY",
  "prompt": "Paste the generated key",
  "secret": true,
  "destinations": [
    {"type": "env", "path": ".env"},
    {"type": "github_secret", "repository": "owner/repo"}
  ]
}
```

- `name` must match `[A-Z][A-Z0-9_]*`.
- A secret may use `env`, `github_secret`, or `none`.
- A secret may never use `github_variable`.
- A public value may use `env`, `github_variable`, or `none`.
- The manifest never contains the captured value.

### `command`

```json
{
  "id": "verify",
  "title": "Verify configuration",
  "type": "command",
  "program": "gh",
  "arguments": ["secret", "list", "--repo", "owner/repo"],
  "expected_exit_codes": [0],
  "irreversible": false
}
```

Commands are executable + argument arrays. Shell metacharacters and `Invoke-Expression` are
prohibited. Secret values are not substituted into arguments.

An irreversible command additionally requires:

```json
{
  "irreversible": true,
  "confirmation_phrase": "APPLY MIGRATION",
  "rollback": "Restore the snapshot described in ..."
}
```

### `pause`

```json
{
  "id": "wait",
  "title": "Wait for propagation",
  "type": "pause",
  "seconds": 10
}
```

The duration must be bounded from 1 to 3600 seconds.

## Validation invariants

- At least one stage exists.
- IDs and capture names are unique.
- Every stage has `id`, `title`, and valid `type`.
- URLs and repository identifiers are literals or explicit non-secret placeholders.
- No manifest key or value resembles a credential.
- Secret values never enter variables, logs, command arguments, or hashes.
- Every irreversible command has confirmation and rollback text.
