# ChatGPT Project + GitHub Deployment

ChatGPT Projects keep project chats, files, and project-specific instructions together. OpenAI also documents a GitHub app that can read authorized repositories and retrieve live code and documents. Feature availability can vary by plan or workspace.

Official references:

- https://help.openai.com/en/articles/10169521-projects-in-chatgpt
- https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt

## Project setup

1. Create a ChatGPT Project for the repository or long-running program.
2. Connect the GitHub app and authorize only the repositories required for the work.
3. Add the following project instruction, adapting only the repository name:

```text
For engineering workflow requests, first read the repository AGENTS.md. Resolve
`docs/implementation/ACTIVE_TASKS.yaml`, the selected task_state.yaml and HANDOFF.md, then read the
pinned Bullbase workflow router at `.agents/workflow-skills/skills/workflow-router/SKILL.md` or its
source-repository equivalent. Treat task_state.yaml as canonical. ChatGPT Web is Supervisor;
GitHub Actions is Executor. Continue in AUTO unless DECISION_POLICY requires a HUMAN_GATE.
```

4. In the consumer repository, install a pinned release using `CONSUMER_INSTALL.md`.
5. Keep `.devflow/workflow-skills.lock.json` under review so a fresh chat can resolve the exact skill revision without relying on memory.

## Resume smoke test

Start a new project chat containing only a task ID. A successful deployment finds the active-task index, state and handoff, reports the current frontier, and continues without asking for the task history again.
