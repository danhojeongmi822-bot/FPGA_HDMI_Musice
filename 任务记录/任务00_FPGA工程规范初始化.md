# 任务 00：FPGA 工程规范初始化

归档日期：2026-10-15。状态：完成。

## 目标与修改前情况

初始化后的 Trellis 使用 Web 前后端模板，缺乏当前 Verilog/安路 TD 工程的真实规范。用户要求完成第 0 个任务，为后续持续开发与对话留档建立基础。

## 具体改动

|改动|相关位置|用途|
|---|---|---|
|建立 FPGA 规范索引|.trellis/spec/index.md、fpga/index.md|明确实际工程类型及修改前/提交前检查|
|整理架构、源引用与加密 IP 约束|fpga/architecture.md|指明板级顶层、数据链路、SDRAM 同名模块和兼容头文件约束|
|整理时钟复位契约|fpga/clock-reset.md|保存 PLL 实际频率、相位、16 拍复位释放及像素/FIFO 约定|
|整理板卡和素材接口|fpga/board-interface.md|保存引脚、按键、数码管极性和物理扇区扫描限制|
|建立验证门禁|fpga/verification.md|区分仿真、引脚报告、用户实板反馈和时序签核|
|建立持续历史记录约定|fpga/history-workflow.md、AGENTS.md|规定后续工作区、任务及日志维护方式|
|移存不适用的 Web 模板|任务00/template-reference/|保留初始化参考，不再放在活动规范中|

表中的 fpga/ 均位于 .trellis/spec/fpga/。当前工程目录为 HX4S20_HDMI/，根目录保留 Trellis、说明及任务记录。

## 实际效果

后续修改可以按真实硬件和当前代码约定执行，避免继续套用 Web 模板。规范明确保存 SDRAM 时序尚未通过、内部音阶不等于 TF 文件播放、数码管状态码不是图片编号等重要事实。本任务只建立开发与记录规则，没有改变 RTL 或板卡运行效果。

## 验证与证据

Trellis 已识别 fpga 规范层；活动规范无未填写模板；任务 implement.jsonl 和 check.jsonl 各 3 条引用校验通过，任务已归档 completed。

- [规范入口](../.trellis/spec/index.md)
- [原任务需求与完成清单](../.trellis/tasks/archive/2026-10/00-bootstrap-guidelines/prd.md)

## 限制及后续

规范描述当前工程及已知问题，不代表全部硬件签核通过。后续代码变化后应同步更新规范、Trellis 和任务记录。Git 尚未提交，任务完成指记录及规范已经落盘。
