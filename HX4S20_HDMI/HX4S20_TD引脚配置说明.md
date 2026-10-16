# HX4S20：安路 TD 引脚配置与使用说明

本次以用户确认的《HX4S20开发板手册-HDL版2410》为板卡依据，器件为 **EG4S20BG256**，工具为 Tang Dynasty 6.2.168116。默认使用板上 **HDMI A** 接口。

**引脚配置已完成，已实际运行综合、布局布线并生成位流；当前时序检查未通过，尚未上板实测。生成位流不等于图片和音频功能已验证。**

## 1. 打开哪个工程

在 TD 中打开本目录下 `HX4S20_HDMI_Config.al`。该工程的顶层是 `hx4s20_board_top`，器件是 `EG4S20BG256`。

原 `Licheng_Pro.al` 及其构建目录已从当前工程移出，归档至上一级 `工程整理备份_20261015`。当前保留 `HX4S20_HDMI_Config.al` 作为工程入口。该工程使用本目录应用源码、板卡适配层和约束，不需要在 TD 中重新手工分配下表引脚。工程文件应与源码目录一起保留，不要单独移动 `.al`。

| 文件 | 用途 |
| --- | --- |
| `HX4S20_HDMI_Config.al` | 已注册约束和适配顶层的 TD 工程 |
| `board/hx4s20_board_top.v` | 板卡顶层，实例化原 `top`，适配数码管位选 |
| `constraints/hx4s20_hdmi_a.adc` | 30 个顶层信号的引脚、电平约束 |
| `constraints/hx4s20_clocks.sdc` | 50 MHz 输入时钟及 PLL 时钟自动推导 |
| `board/build_project.tcl` | 本次实际使用的直接构建流程 |
| `board/build_console_single.log` | 实际构建日志 |
| `board/pin_verification.json` | ADC 与最终 IO 报告逐项核对结果、位流 SHA256 |
| `build_hx4s20/route.area` | 布线后 IO 分配、电平和资源使用报告 |
| `build_hx4s20/route_timing.rpt` | 布线后完整时序报告 |
| `build_hx4s20/HX4S20_HDMI_Config.bit` | 已生成的实验位流；仍有时序违例 |

## 2. 引脚表

除 HDMI 高速差分输出使用官方例程的 **LVDS33** 外，以下用户信号均为 **LVCMOS33**。

| 顶层信号 | FPGA 球位 | 板上功能 |
| --- | --- | --- |
| clk | R7 | 50 MHz 板载时钟 |
| rst_n | A2 | KEY1，低有效复位 |
| key1 | B2 | KEY2，下一张图片 |
| key2 | B1 | KEY3，自动轮播控制 |
| sd_ncs | A12 | TF 卡片选，SPI 模式 |
| sd_dclk | A14 | TF 卡 SPI 时钟 |
| sd_mosi | A13 | FPGA 向 TF 卡发送数据 |
| sd_miso | B14 | FPGA 从 TF 卡接收数据 |
| HDMI_CLK_P | K1 | HDMI A 时钟正端，负端 J1 |
| HDMI_D0_P | F5 | HDMI A 数据 0 正端，负端 F4 |
| HDMI_D1_P | E3 | HDMI A 数据 1 正端，负端 E4 |
| HDMI_D2_P | B3 | HDMI A 数据 2 正端，负端 D3 |
| HDMI_DDC_SCL | P1 | HDMI A DDC 时钟 |
| HDMI_DDC_SDA | R1 | HDMI A DDC 双向数据 |

TD 根据 LVDS33 自动生成四路配对负端；最终报告已确认是 J1、F4、E4、D3，无须在 Verilog 顶层再增加同一组负端端口。DDC 按板卡电路使用 3.3 V 逻辑接口。

| 下标 | seg_sel 球位 | seg_data 球位 | 段信号 |
| --- | --- | --- | --- |
| 0 | F16 | C15 | a |
| 1 | E16 | C16 | b |
| 2 | E12 | B6 | c |
| 3 | E10 | A5 | d |
| 4 | C13 | B5 | e |
| 5 | F10 | A8 | f |
| 6 | E11 | A7 | g |
| 7 | D11 | A6 | DP |

板卡有 8 位数码管，位选高有效、段选低有效；原程序扫描器输出 6 位低有效位选。适配层使用 `seg_sel = {~app_seg_sel_n, 2'b00}`，将左侧两位关闭，其余六位连接原扫描器。板上 **SW6 拨上选择数码管**；数码管与双色 LED 存在复用。

KEY4（C1）当前未使用。SDRAM 使用 `EG_PHY_SDRAM_2M_32` 硬原语，相关内部专用连接由器件工具处理，不需要另配外部 SDRAM 用户引脚。音频由现有逻辑内部产生，通过同一个 HDMI 输出，本次没有新增音频输入引脚或 TF 音频文件播放器。

## 3. 为让工程可编译做的调整

- 在独立工程中恢复此前被自动排除的必要 HDL、PLL、FIFO 和加密 IP 文件。
- 从新工程文件列表移除 `IP/sdram.v` 的重复引用，保留接口匹配应用的 `SD/sdram.v`。两个文件在磁盘上均保留，原工程未覆盖。
- 增加 `user_source/hdl_source/include/global_def.v` 兼容副本，满足原 SDRAM 文件的历史相对 include 路径；加密控制器内容未修改。以后修改全局宏时，需要同步此副本与 `include/global_def.v`。
- SDC 加入 20 ns 输入时钟和 `derive_clocks`。这是基础时钟约束，尚不构成完整 IO、跨时钟和 SDRAM 时序签核。没有用全局 false path 隐藏违例。

## 4. 本次实际验证结果

2026-10-15 使用 TD 6.2.168116 直接运行 `board/build_project.tcl`，完成实际综合、布局、布线和位流生成。

| 检查项 | 结果 |
| --- | --- |
| 顶层器件 | hx4s20_board_top / EG4S20BG256 |
| 30 个顶层信号 | 全部与 ADC 的位置、电平一致 |
| 四个 HDMI 负端 | 自动分配正确，与正端共同占用 34 个用户焊盘 |
| 引脚重复 | 用户引脚及差分配对间无重复 |
| 位流文件 | 已生成，629637 字节 |
| LUT / 寄存器 | 4237 / 3880 |
| BRAM / PLL | 20 / 3 |
| 最差建立裕量 SWNS | **-6.699 ns，未通过** |
| 建立总负裕量 STNS | -296.354 ns |
| 最差保持裕量 HWNS | 0.019 ns |
| STA 覆盖率 | 99.63%，仍有未覆盖路径 |
| 实际板上验证 | 未执行 |

当前主要时序问题涉及 SDRAM 的 125 MHz 域和关联路径，100 MHz 域也有负裕量。构建中还存在原有端口位宽、未驱动网络/寄存器时钟及 SDRAM 原语位置被工具调整的告警。需要结合原控制器、CDC 和器件专用时序要求继续核查；不能简单地以位流可生成判断功能正确。

命令行工程模式的 `launch_runs` 曾生成错误的 `td_commands_prompt_commands_prompt.exe` 启动路径，且在没有真实综合产物时打印 success。因此本次最终以直接 Tcl 流程及 `build_console_single.log`、`build_hx4s20` 中的真实产物作为依据。不要把较早的 `build_console.log` 当作成功证据。

可复现命令（PowerShell）：

```powershell
& 'D:/Anlogic/TD_6.2.1_Engineer_6.2.168.116/bin/td_commands_prompt.exe' 'C:/Users/cheng/Desktop/FPGAVrlog/ATask999_CPDLICHENG/board/build_project.tcl'
python 'C:/Users/cheng/Desktop/FPGAVrlog/ATask999_CPDLICHENG/board/verify_pin_report.py'
```

## 5. 接板与下载

1. 使用 TD 打开 `HX4S20_HDMI_Config.al`，核对器件和顶层。约束已加入，不要再次导入一份。
2. 显示器接板上 **HDMI A**，插入此前准备的 TF 卡，并给开发板供电。需要数码管显示时将 SW6 拨上。
3. 使用板卡下载接口/下载器，在 TD Programmer 中识别目标器件后选择对应位流。HDMI 负责视频/音频输出，不能代替下载连接。
4. 当前生成的 `.bit` 可用于有上述限制的实验调试；建议先处理时序违例，再作为稳定版本使用。本次未替用户执行实际下载，也未配置上电 Flash 固化。
5. 复位使用板上 KEY1；KEY2 对应程序的 key1（下一张）；KEY3 对应 key2（自动轮播）。若黑屏，先检查接口是否为 HDMI A、输入源和复位，再结合时序及 TF/SDRAM 链路排查。

本次仅完成硬件引脚适配，未改变 TF 文件读取机制和图片格式要求，也未验证卡片数据、图片扫描和 HDMI 接收端兼容性。

## 6. 资料依据

- 用户明确确认的 `资料与开发板原理图与说明/10_康芯开发板使用手册及实验平台/HX4S20开发板手册-HDL版2410.pdf`。
- 本机厂商实验包 `HXEG420C_lab_ex_TD6.2.1版本制作.zip` 中 `HXEG420_lab_ex/lab_ex_6_tf_sdram_hdmi/top.adc`，用于交叉核对 TF、HDMI 球位及 LVDS33 电平。
- 安路 TD Tcl Command User Guide 的 single_run 构建流程及本次布线后 IO 报告。

曾执行联网搜索，但未获得可独立确认的同版本公开管脚文档。最终引脚依据为上述指定手册与本机厂商例程；未采信搜索引擎中不相关的型号结果，也未照搬资料中混入的 Quartus 时序脚本。
