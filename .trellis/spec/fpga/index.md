# FPGA 开发规范

## Pre-Development Checklist

1. 阅读当前任务 prd.md、design.md、implement.md，确认本次变更边界。
2. 阅读 [架构](architecture.md)、[时钟与复位](clock-reset.md)。改引脚或卡片准备时加读 [板卡接口](board-interface.md)。
3. 阅读 [验证门禁](verification.md) 和 [历史管理](history-workflow.md)。
4. 阅读 ../guides/index.md。先搜索已有实现，再修改 RTL/IP/约束。

## Quality Check

- 在仓库根运行 python HX4S20_HDMI/board/verify_pin_report.py 和 python HX4S20_HDMI/board/run_regression.py。后者默认读取 HX4S20_HDMI/assets/tf/001.bmp～004.bmp。
- 修改 RTL、PLL、ADC、SDC 后需重新执行 TD 综合/布局/布线/STA/bitgen，关联位流哈希。迁移只改路径可复用历史报告，但必须明确未重新构建。
- 查验任务上下文路径、索引、测试结果和用户反馈；不得将初测正常记成时序签核通过。
