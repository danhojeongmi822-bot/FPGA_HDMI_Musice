> 路径约定：以下源码、素材、构建产物路径均相对 HX4S20_HDMI/；Trellis 与 docs 路径相对工作区根。当前 TD 入口 HX4S20_HDMI/HX4S20_HDMI_Config.al。

# Trellis 历史与迁移约定

后续工作区为 C:/Users/cheng/Desktop/FPGAVrlog/AEnd_the_game，入口 HX4S20_HDMI/HX4S20_HDMI_Config.al。原 ATask999_CPDLICHENG 保留回退，不再作为新修改入口。应用窗口需用户切换打开新目录，脚本明确指定新工作目录。

任务 00 完成 FPGA 开发规范初始化。任务 01 为验证官方例程，整理此前对话、工程迁移及实板初测，当前代码作为后续独立优化任务的基线：历史整理属于可见消息及工程证据的摘要，不伪称逐字导出。以后每次任务记录需求、决策、变更、验证、用户反馈、限制与下一步，并追加开发者 journal。

记录中区分“用户报告”“本轮工具验证”“历史报告”“推断/待确认”。保留原始报告时间和内容，用新文档补充新结论；不要全局替换历史日志里的旧路径。迁移清单 board/migration_manifest.json 保存原文件哈希，预期改变的文件必须列出原因。

任务上下文 implement.jsonl/check.jsonl 引用真实 spec/research 文档，归档后检查引用仍可解析。脚本 task.py archive --no-commit 和 add_session.py --no-commit 允许本次按用户要求先完成磁盘记录，Git 提交单独审核；不伪造提交哈希。历史导入任务无 PR，使用 --skip-branch-validation 时在任务结果说明原因。Git 提交前遵循 .trellis/workflow.md 第 3.4 节一次性具体计划确认。

## 目录修正（2026-10-15，用户明确要求）

工作区一级保留 Trellis、配置、README 和 docs 工程说明；完整工程作为二级 HX4S20_HDMI/。TD Project Path 指向工程子目录。后续不得平铺 RTL、IP、素材和报告到工作区根。初次迁移和 Session 1 的旧路径只作历史，当前入口以 README 为准。

## 每个任务的改动与效果记录

工作区一级任务记录/保存人工可读的独立Markdown，命名任务NN_任务名称.md。每次任务开始时建立文件，结束时补齐改动、实际效果、验证证据、限制和后续工作，更新任务记录/README.md并链接Trellis。未测结果不得写成已通过。当前已补齐任务00及任务01，后续优化另建编号。
