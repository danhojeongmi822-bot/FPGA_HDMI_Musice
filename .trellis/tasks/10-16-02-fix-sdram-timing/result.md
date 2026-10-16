# 任务02执行结果（2026-10-16）

状态：代码修改、TD重新构建、当前约束下STA与针对性回归完成；新位流整机实板待验收，任务保持in_progress。不代表完整IO/CDC签核通过。

## 根因与修复

1. 原SDRAM逻辑/器件时钟125MHz相差180°，双向各4ns预算。读路径含SDRAM硬核5ns输出延迟、PAD输入寄存器及器件时钟PAD/局部布线偏差，最差-6.699ns；写数据/三态使能方向同样不满足。调整真实PLL C1/C2为41.666667MHz，分频24、相位参数23/11，周期24ns、半周期12ns。C0仍100MHz，视频与音频PLL不变。两份global_def.v的SDR_CLK_PERIOD同步24。
2. 第一次降频重建SDRAM已转正，但mem→TF写应答仍-0.500ns，具体进入bmp_read状态机。frame_read_write.v在write_clk/read_clk各加两级返回应答同步，控制器应答保持到请求撤销，适合电平握手。未增加false path、未改加密控制器。
3. 未驱动clk告警出现在optimize_gate的PAD寄存器合并阶段。探查网表旧Sdr_rd_dout_reg[0..31]均clk常量0、无Q输出，真正采样已并入EG_PHY_PAD（IN_DFFMODE=FF、INPCLKMUX=CLK、ipclk接Sdr_clk）。最终legalize_phy_inst之后导出的gate.v无旧寄存器，32位有效采样完整。原始日志仍有告警，不能声称告警文字消失。去包装层keep的试验无效，已恢复原包装层。

## 结果与证据

工程根为HX4S20_HDMI/，以下路径相对此根。

|项目|原基线|正式修复构建|
|---|---|---|
|全局SWNS/STNS|-6.699/-296.354 ns|+0.133/0 ns|
|全局HWNS/HTNS|+0.019/0 ns|+0.003/0 ns|
|SDRAM逻辑捕获组SWNS|-6.699 ns|+0.725 ns|
|SDRAM移相捕获组SWNS|-2.842 ns|+5.120 ns|
|STA覆盖率|99.63%|99.64%|

正式TD：6.2.168116，慢/快角setup/hold均检查；build_hx4s20/route_timing.rpt、route_timing_status.rpt、route.area、gate.v；完整日志board/task02/final_build_console.log。最小保持裕量很小，需保持约束审查与实板验证边界。

正式位流build_hx4s20/HX4S20_HDMI_Config.bit，629637字节，SHA256 d4cceb63350dc5be526d4af7bd311d6fff7d15d06a003fb5ac1c1cf3abe5f531。

原位流board/task02/baseline/build_hx4s20/HX4S20_HDMI_Config.bit，SHA256 7ab4088df366c4aa64b764e9ca3ec67cebeb56d7f9d67caf8d520f8b0ffddaea。回退PLL/宏时使用同目录源码快照；frame_read_write.v新增同步与降频可独立回顾。

8项回归通过：视频、音频、复位、跨域应答、四张实际BMP逐像素核对。tb_frame_ack使用真实读写状态机、空FIFO桩，仅验证同步/保持/撤销/复位，轮次间复位，不覆盖帧完成或真实FIFO吞吐。原先等待桩模拟的帧完成导致测试超时，修正测试范围后通过。

verify_pin_report.py核对30个显式信号+4个自动差分负端，reported_timing_checks_passed=true、完整timing_signoff_passed=false；verify_sdram_mapping.py核查32位有效采样、最终旧寄存器为0、24ns参数同步，结果JSON关联位流及gate.v哈希。

## 降频适配与限制

SDRAM每周期32位，41.667M字/秒；视频有效期间25M像素/秒、一像素一字，平均约18.286M字/秒。TF SPI仍25MHz，理论输入像素上限约1.042M字/秒；256字写突发至少约6.14us，FIFO与仲裁额外间隔需要实际长稳确认。上述为吞吐预算而非完整硬核仿真证明。

刷新宏为64000000/24/2048=1302，计数周期约31.272us；首次预上电计数2^17周期约3.146ms，降频后等待更长。保留原固定周期初始化/读流水，低频下时间间隔增长；不声称核内时序已全部仿真。未改任何加密文件。HDMI仍25/125MHz，音频仍内部测试音。

## 待实板验收

按docs/任务02_上板验收.md烧录上述新位流，逐项记录冷启动、全四图、复位、切图、轮播启停、声音和长稳。当前无该新位流实测反馈，不归档为整机完成。Git仓库尚无提交，未自动stage/commit。
