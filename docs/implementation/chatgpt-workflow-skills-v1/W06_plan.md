# W06 Plan — PowerShell Manual Wizard

## Objective
Implement a PowerShell-first, idempotent, secret-safe generator for unavoidable human setup.

## Outputs
- `skills/manual-wizard-powershell/SKILL.md`
- reusable PowerShell wizard library/template
- static validator and example stage manifest
- W06 result/state updates

## Gate
The script must parse under PowerShell syntax rules by inspection/static checks, hide secrets,
avoid logging values, verify destinations, support reruns, and require confirmation only for
irreversible actions.
