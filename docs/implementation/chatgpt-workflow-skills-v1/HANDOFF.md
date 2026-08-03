# Durable Handoff

## Task identity

- **Task ID:** `chatgpt-workflow-skills-v1`
- **Repository:** `BullbaseGuy/chatgpt-workflow-skills`
- **Branch:** `agent/chatgpt-workflow-skills-v1`
- **Canonical state:** `docs/implementation/chatgpt-workflow-skills-v1/task_state.yaml`
- **Dependency graph:** `docs/implementation/chatgpt-workflow-skills-v1/dependency_graph.yaml`

## Destination

Deliver and validate ten reusable skills, their shared references/templates, historical
regression scenarios, dual ChatGPT deployment paths, and a non-duplicating integration
with `BullbaseGuy/demo-project`.

## Verified completed

- W00 adoption baseline and license reconciliation are complete.
- The upstream source revision and scaffold baseline are pinned.
- The repository contract, glossary, ADR, adoption matrix, conflict resolutions, canonical
  task state, dependency graph, and handoff entry point exist.
- Codex/model invocation count remains `0`.

## Current frontier

- `W01` — terminology, state, failure, and decision model.

## Active blocker

None.

## Exact next action

Read `W01_plan.md` when present, implement the seven shared reference documents and five
templates, validate their internal links and YAML examples, write `W01_result.md`, then move
the frontier to W02 without asking the user to continue.

## Resume rule

A new session receiving only the task ID, an Issue/PR URL, or an Actions URL must resolve
this file through `ACTIVE_TASKS.yaml`, read canonical state, verify the remote run/branch,
and continue from the frontier. It must not ask the user to restate prior decisions.
