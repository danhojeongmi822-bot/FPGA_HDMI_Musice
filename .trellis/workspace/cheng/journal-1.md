# Journal - cheng (Part 1)

> AI development session journal
> Started: 2026-10-15

---



## Session 1: 任务01：验证官方例程与工程迁移交接
<!-- trellis-session: v=2 fp=acdf0202b3e614cf -->

**Date**: 2026-10-15
**Task**: 任务01：验证官方例程与工程迁移交接
**Branch**: `master`

### Summary

完成FPGA规范初始化，记录官方例程验证历史和用户实板初测，迁移工程作为后续优化基线。

### Main Changes

# 本次会话：验证官方例程与工程交接

用户明确第一个任务为“验证官方例程”，后续基于当前代码优化，另建任务。本次将已有对话整理为结构化历史摘要，并完成工程交接；没有导出逐字完整聊天。

- 任务00：根据真实Verilog/TD工程建立FPGA规范，原Web模板移存任务00参考目录。
- 任务01：整理例程功能、引脚/PLL/复位适配、历史外围修复和验证证据；用户反馈显示、复位、手动切图、自动轮播大体正常。
- 新工作区：C:/Users/cheng/Desktop/FPGAVrlog/AEnd_the_game，TD入口HX4S20_HDMI_Config.al。原ATask999_CPDLICHENG保留回退。应用需打开新目录，当前工具均在新目录执行。
- 迁移首次复制84个文件并逐项哈希核对，79个保持原样，5个预期改变：工程根Path、回归素材默认路径、两份重跑结果JSON、历史核查文档追加说明。附加素材制作脚本与卡布局历史报告另行哈希核对。39个工程引用均存在，RTL/PLL/约束/位流不变。
- 本轮运行7次针对性仿真全部通过：视频3840像素/6TLAST/2SOF；音频42样本/41非零及复位；16沿复位释放与丢锁；4张BMP各307200像素逐值一致。30显式引脚加4自动差分负端匹配历史最终IO报告。
- 位流629637字节，SHA256：7ab4088df366c4aa64b764e9ca3ec67cebeb56d7f9d67caf8d520f8b0ffddaea。此为保留文件哈希，未确认用户实际烧录的就是该哈希。
- 本轮没有完整重建TD、下载或写F盘。SDRAM SWNS -6.699ns仍未通过时序；音频实测、冷启动/长稳、完整四图顺序、多位数码管显示与AXIS背压仍待后续任务。状态1/2是运行状态而非图片编号。
- 对话、现象对照、迁移说明分别见docs/对话历史整理.md、docs/上板现象对照.md、docs/工程迁移说明.md；迁移与用户反馈JSON位于board/。
- Git尚无提交，所有记录先落盘。归档和journal均显式使用--no-commit，历史导入无PR使用--skip-branch-validation。--commit -表示没有关联提交，不表示只做规划；未执行要求代码先提交的完整finish-work。Git提交前依workflow第3.4节单独审核具体计划。

后续：以当前迁移代码作为优化基线，独立任务逐项处理SDRAM时序及体验问题；每次继续补记Trellis任务和cheng journal。


### Git Commits

(No commits - planning session)

### Status

[OK] **Completed**


## Session 2: 任务01补充：整理工程层级与每次任务说明
<!-- trellis-session: v=2 fp=8af5b5ae0f1cd539 -->

**Date**: 2026-10-15
**Task**: 任务01补充：整理工程层级与每次任务说明
**Branch**: `master`

### Summary

工程收进HX4S20_HDMI，一级新增任务记录目录，补齐任务00和01的改动与效果说明。

### Main Changes

# 目录整理及任务说明补充

用户要求一级保留Trellis和工程说明，工程放第二级，并新增文件夹详细记录每次任务改动和效果。

- 将24个工程条目整体收进HX4S20_HDMI/；93文件移动前后哈希一致。TD Project Path已更新，RTL/PLL/ADC/SDC/位流不变。
- 新目录重新运行7次针对性仿真全部通过，30显式引脚加4自动差分负端匹配报告，39工程引用有效。未重新TD构建、烧录或写TF卡。
- 一级新增任务记录/，补齐任务00_FPGA工程规范初始化.md、任务01_验证官方例程.md和索引，记录改动、效果、证据、限制及后续工作。
- README、AGENTS、规范和任务01交接记录同步。目录整理属于任务01补充，未另开优化任务。
- SDRAM时序、长期稳定性等原有待办保留。所有记录落盘，未Git提交。


### Git Commits

(No commits - planning session)

### Status

[OK] **Completed**


## Session 3: 任务02修复SDRAM时序与读写握手
<!-- trellis-session: v=2 fp=015212f69c76d5f1 -->

**Date**: 2026-10-16
**Task**: 任务02修复SDRAM时序与读写握手
**Branch**: `master`

### Summary

将SDRAM C1/C2降为41.667MHz并同步周期参数，为TF与SDRAM读写应答增加两级接收同步；正式STA由-6.699ns改善为SWNS +0.133ns，8项回归和网表核查通过，整机实板待验收。

### Main Changes

- 完成SDRAM时序与映射网表分析
- 生成正式位流并保存哈希
- 增加跨域握手回归与SDRAM映射核查

### Git Commits

(No commits - planning session)

### Testing

- [OK] TD正式构建、STA与bitgen通过
- [OK] 视频、音频、复位、握手和四张BMP回归通过

### Status

[OK] **Completed**

### Next Steps

- 用户烧录新位流并按docs/任务02_上板验收.md完成冷启动与长稳验收
