# Repository Agent Contract

本文件是 ChatGPT Web 与其他受控 agent 的仓库级入口。

## Required reading order

1. `references/USER_OPERATING_CONTRACT.md`（存在后）；
2. `references/DECISION_POLICY.md`（存在后）；
3. `docs/implementation/ACTIVE_TASKS.yaml`；
4. 活跃任务的 `task_state.yaml`、`HANDOFF.md` 与当前 `Wxx_plan.md`；
5. 被调用技能的 `SKILL.md`；
6. 该技能明确指向的公共 reference；
7. 当前分支、Pull Request 与 GitHub Checks。

## Non-negotiable rules

1. ChatGPT Web 是 Supervisor；GitHub Actions 是 Executor。
2. `task_state.yaml` 是 canonical task state；聊天记录不是状态库。
3. 每个工作包实施前必须存在 `Wxx_plan.md`，通过确定性验证后才能写 `Wxx_result.md`。
4. 低风险且可逆的决策使用 `AUTO`；只有权限、密钥、不可逆操作、重大业务/投资选择或无法自动裁决的权威来源冲突才能进入 `HUMAN_GATE`。
5. 可恢复错误必须先建立 tight feedback loop、复现并分类，再进行有界重试。
6. 已完成 checkpoint 不得重跑；单一阻塞不得无故冻结其他 frontier。
7. Codex/模型执行默认关闭。本任务目标调用数是 `0`。
8. 人工操作优先提供 PowerShell，不默认要求 Bash。
9. 已存在于对话、仓库、状态、Issue、PR 或日志中的事实不得重复询问。
10. 不使用 Gmail 或外部邮箱作为执行依赖。
11. 不在任何持久化表面写入秘密、私有端点或可用于推导秘密的转换值。
12. 所有完成声明必须同时有 Standards、Spec 与 Evidence 证据。
13. 不得声称异步或后台工作仍会在未来自动交付；未完成工作必须成为显式任务状态。
14. 规则只在一个权威位置定义；技能应通过 context pointer 引用，而不是复制。
