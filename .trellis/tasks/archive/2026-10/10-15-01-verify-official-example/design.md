# 迁移设计

最小差距：旧工程缺少新 Trellis 仓库中的工程与历史，且回归依赖旧例程目录。真实变更位置为新仓库根的工程文件、board/run_regression.py 和 Trellis 文档。

保留单工程根布局，不再嵌套复制一层目录。.al 的 Project Path 指向新根，所有源/约束仍相对定位。排除旧入口 Licheng_Pro.al、.lock.f、*_Runs、log 缓存和 .vvp；保留 build_hx4s20 产物、board 构建日志作为可审计证据。四张图片复制到 assets/tf，回归默认值改为 base/assets/tf。原目录不动。

不修改 RTL、PLL、引脚约束或位流。报告里的旧绝对路径保留历史真实性；重跑的 JSON 明确为当前检查。用户实测独立存档，不把 pin_verification.json 的 board_test_performed=False 改成代理亲测通过。

第 00 任务重塑规范；第 01 任务记录对话及迁移结果。使用脚本完成归档与 journal，禁用这次自动 Git 提交。
