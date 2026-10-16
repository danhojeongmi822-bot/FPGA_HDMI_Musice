# 执行与检查

1. 读取实际源码、旧报告、Trellis 工作流和任务脚本。
2. 复制必要文件并逐项 SHA-256 核对，记录 board/migration_manifest.json。
3. 适配 .al 根路径及回归素材默认路径，不改 RTL；建立 FPGA 规范及任务历史。
4. 新根运行 python board/verify_pin_report.py、python board/run_regression.py；验证全部工程引用、BMP 头、哈希、相同头文件和无旧工程入口。
5. 校验 jsonl 上下文与 Markdown 本地引用。
6. task.py archive 两个任务，均使用 --no-commit；历史导入没有 PR，使用 --skip-branch-validation 并保留说明。
7. add_session.py 追加 cheng 会话；没有 Git 工作提交，--commit -，明确是未提交的历史迁移记录。

完整 TD 重建不在路径迁移验收内，现有时序违例原样保留。后续若开展时序修复，必须另建任务并重新构建。
