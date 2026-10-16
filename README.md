# HX4S20 TF 图片与 HDMI 演示工程

工作区根目录负责 Trellis、工程介绍与历史记录；完整 FPGA 工程统一位于 HX4S20_HDMI/。

```text
AEnd_the_game/
├── .trellis/          任务、规范、对话与会话日志
├── 任务记录/          每个任务的改动、效果和验证
├── AGENTS.md          协作约定
├── README.md          工程介绍与入口
├── docs/              对话整理、上板对照和迁移说明
└── HX4S20_HDMI/        完整 TD 工程
    ├── HX4S20_HDMI_Config.al
    ├── board/         板级适配、构建及验证脚本
    ├── constraints/   ADC/SDC 约束
    ├── SD/、IP/、include/、user_source/
    ├── assets/tf/     四张 BMP 测试素材
    └── build_hx4s20/  位流与历史构建报告
```

Git 及 Trellis 初始化的隐藏工具目录保留在工作区根目录。

本工程在用户 HX42S20 板卡（对应 HX4S20 HDL2410 手册、EG4S20BG256）上从 TF 卡扫描 BMP，缓存到 SDRAM，经 HDMI A 输出 640×480 图像，支持手动切图和自动轮播。HDMI 音频为内部音阶测试音，不读取卡上的 MP3/WAV。

在安路 TD 6.2.168116 打开 [工程文件](HX4S20_HDMI/HX4S20_HDMI_Config.al)，顶层 hx4s20_board_top。[实验位流](HX4S20_HDMI/build_hx4s20/HX4S20_HDMI_Config.bit)与 RTL 未因目录整理改变。

- [任务记录索引](任务记录/README.md)
- [上板现象对照](docs/上板现象对照.md)
- [任务02 SDRAM 最优方案研究](docs/任务02_SDRAM最优方案研究.md)
- [对话历史整理](docs/对话历史整理.md)
- [工程迁移与目录说明](docs/工程迁移说明.md)
- [Trellis 任务索引](.trellis/tasks/index.md)
- [开发规范](.trellis/spec/index.md)
- [会话日志](.trellis/workspace/cheng/index.md)

任务 00 为规范初始化；任务 01 为验证官方例程，用户反馈显示和主要按键功能初测大体正常。任务 02 已将正式构建的 SDRAM STA 建立裕量改善为 SWNS +0.133 ns，并保留完整实板验收为待办；STA 和仿真通过不等于整机长期稳定性验收。

在工作区根目录执行检查：

```powershell
python HX4S20_HDMI/board/verify_pin_report.py
python HX4S20_HDMI/board/run_regression.py
```

也可进入 HX4S20_HDMI 后使用 python board/… 命令。四张素材在 HX4S20_HDMI/assets/tf/，为 640×480、24 位无压缩正高度 BMP。硬件按物理扇区扫描，卡上文件需位于扫描范围且数据连续；文件名不控制硬件读取顺序。
