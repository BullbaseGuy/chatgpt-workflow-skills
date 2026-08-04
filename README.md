# Bullbase ChatGPT Workflow Skills

面向 **ChatGPT Web Supervisor + GitHub Actions Executor** 的可复用技能体系。

本仓库是跨项目技能、公共规则、状态契约、证据结构和安装逻辑的唯一来源。
`BullbaseGuy/demo-project` 只保留工程脚手架与引用，不复制维护技能正文。

## 核心约束

- ChatGPT Web 负责理解、规划、诊断、审查和恢复决策；
- GitHub Actions 负责确定性执行、验证、状态检查和有界恢复；
- `task_state.yaml` 是任务状态唯一事实源；
- 每个工作包先写 `Wxx_plan.md`，验证后再写 `Wxx_result.md`；
- 可恢复错误先诊断再重试，禁止盲目重跑；
- 低风险可逆决策默认 `AUTO`，人工检查点尽量后移；
- Codex/模型执行默认关闭，当前目标调用数为 `0`；
- Windows PowerShell 是人工操作的首选入口；
- 任何秘密、私有端点或可逆推出秘密的信息都不得进入版本库、Issue、PR、日志或 artifact。

## 目录

```text
skills/                  可组合 SKILL.md
references/              跨技能唯一事实源
templates/               任务、交接、失败、人工门和验收模板
scripts/                  确定性验证与 PowerShell 安装工具
tests/scenarios/          历史回归场景
docs/implementation/     本仓库任务状态与阶段证据
docs/deployment/         ChatGPT Skills / Project 双路径部署
```

## 使用入口

1. 阅读 `AGENTS.md`；
2. 运行或选择 `workflow-router`；
3. 由路由器按任务类型调用其他技能；
4. 新会话从 `task_id`、Issue、PR 或 Actions URL 恢复，不依赖聊天记录作为状态源。

当前建设任务：`docs/implementation/chatgpt-workflow-skills-v1/`。
