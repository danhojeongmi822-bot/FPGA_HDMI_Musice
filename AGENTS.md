<!-- TRELLIS:START -->
# Trellis Instructions

These instructions are for AI assistants working in this project.

This project is managed by Trellis. The working knowledge you need lives under `.trellis/`:

- `.trellis/workflow.md` — development phases, when to create tasks, skill routing
- `.trellis/spec/` — package- and layer-scoped coding guidelines (read before writing code in a given layer)
- `.trellis/workspace/` — per-developer journals and session traces
- `.trellis/tasks/` — active and archived tasks (PRDs, research, jsonl context)

If a Trellis command is available on your platform (e.g. `/trellis:finish-work`, `/trellis:continue`), prefer it over manual steps. Not every platform exposes every command.

If you're using Codex or another agent-capable tool, additional project-scoped helpers may live in:
- `.agents/skills/` — reusable Trellis skills
- `.codex/agents/` — optional custom subagents

Managed by Trellis. Edits outside this block are preserved; edits inside may be overwritten by a future `trellis update`.

<!-- TRELLIS:END -->

# 本工程约定

- 始终使用简体中文回复和维护任务说明。
- 后续工作区为 C:/Users/cheng/Desktop/FPGAVrlog/AEnd_the_game，TD 入口 HX4S20_HDMI/HX4S20_HDMI_Config.al。
- 第 01 个任务是验证官方例程；当前代码是后续优化基线，后续优化另建 Trellis 任务。
- 开始修改前读 .trellis/spec/index.md 与 fpga/index.md；会话结束把需求、决策、验证、用户反馈及遗留问题记入任务与 cheng journal。
- 区分用户实板反馈、代理检查和历史报告；不能把初测正常视为时序签核通过。

- 目录层级：工作区根保留 Trellis 与工程说明，完整 TD 工程统一放在 HX4S20_HDMI/，禁止把源码、IP、约束或构建产物平铺回工作区根。

- 工作区一级保留任务记录/，每个任务使用任务NN_任务名称.md，记录目标、修改前情况、具体改动、实际效果、验证证据、限制和后续工作，并链接到Trellis任务。新增任务时建立对应文件，结束时补齐结果并更新索引；同一任务补充修正追加原记录。
