# W03 Plan — Frontier Planner and Execution Supervisor

## Objective
Implement dependency-aware planning and continuous GitHub Actions supervision without
blind reruns or repeated user prompts.

## Outputs
- `skills/frontier-planner/SKILL.md`
- `skills/execution-supervisor/SKILL.md`
- deterministic state/frontier validators
- GitHub Actions validation workflow
- W03 result/state updates

## Gate
The validator must compute frontier correctly, reject cycles and invalid DONE transitions,
preserve completed checkpoints, and distinguish live heartbeat from a stalled run.
