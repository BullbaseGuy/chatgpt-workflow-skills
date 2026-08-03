# Domain Glossary

| Term | Canonical meaning |
|---|---|
| **Supervisor** | 读取需求与证据、做出路由和决策、维护任务语义的 ChatGPT Web 会话。 |
| **Executor** | 运行确定性命令、测试、验证和有限恢复的 GitHub Actions。 |
| **Skill** | 一个小型、可组合、具有触发条件、步骤、完成条件和失败路径的 `SKILL.md` 工作流单元。 |
| **Reference** | 被多个技能引用的唯一事实源；包含公共规则、schema 或输出契约。 |
| **Context pointer** | Skill 中指向仅在相关分支需要时加载的 reference 路径。 |
| **Task** | 有唯一 `task_id`、canonical state、目标和完成定义的持续工作。 |
| **Work package** | 一条可独立验证的纵向 tracer-bullet，编号为 `Wxx`。 |
| **Blocking edge** | 一个 work package 在开始前必须完成的真实依赖。 |
| **Frontier** | 所有 blocker 已完成、当前可以执行的 work package 集合。 |
| **Checkpoint** | 已完成且有证据、恢复时不得重跑的持久化边界。 |
| **Heartbeat** | 长任务证明仍在前进或至少仍存活的定期状态信号。 |
| **Tight feedback loop** | 已实际运行、能准确命中目标症状、快速、确定且可由 agent 重复执行的红绿判断。 |
| **Human gate** | 只有人类能完成或决定的阻塞边界；必须附最小操作与验证方法。 |
| **Push right** | 在不增加不可接受风险的前提下，将人工检查点推迟到自动工作尽可能完成之后。 |
| **Evidence** | 支撑完成、失败、研究结论或验收判断的可定位事实、命令输出、来源或 artifact。 |
| **Durable handoff** | 存放在仓库中、可让新会话从明确下一步恢复的交接文档。 |
| **Blind rerun** | 在没有新诊断、反馈环、分类或策略变化的情况下重复同一失败执行。 |
