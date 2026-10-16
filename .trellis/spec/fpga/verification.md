> 路径约定：以下源码、素材、构建产物路径均相对 HX4S20_HDMI/；Trellis 与 docs 路径相对工作区根。当前 TD 入口 HX4S20_HDMI/HX4S20_HDMI_Config.al。

# 验证门禁与已知风险

## 可执行检查

从工程目录 HX4S20_HDMI/ 执行（Icarus Verilog 当前安装于 C:/iverilog/bin）：

```powershell
python board/verify_pin_report.py
python board/run_regression.py
```

前者比对 .al、ADC、最终 route.area 的 30 个显式信号、4 个自动差分负端以及位流 SHA-256。它核对保留的报告，不会执行新的 TD 布线。后者运行视频、音频、复位和四张 BMP 共 7 次针对性仿真，结果保存在 board/regression_results.json。不得用退出成功替代查看各测试断言与边界。

TD 构建脚本 board/build_project.tcl 依次执行 elaborate、综合、place、route、STA、bitgen。RTL/PLL/约束改动后必须重建并保存新的报告/位流哈希。build_hx4s20 中现有结果由原目录迁入，本次路径迁移没有重新执行 TD。

## 证据层次

- 单元仿真：保护 IP、实际 TF/SPI、整机背压并未完整覆盖。
- 引脚/构建：完成 bitgen 不等于 STA 通过。
- 用户实板：2026-10-15 用户反馈显示、复位、手动切图与轮播初测大体正常；不是代理亲自测量。实际烧录 bit 的 SHA-256 未提供。
- 长期验收：音频、冷启动、全四图顺序、长时间稳定性和多位数码管现象仍需确认。

## SDRAM 时序现状

历史报告 SWNS -6.699 ns、STNS -296.354 ns、HWNS 0.019 ns、覆盖率 99.63%，未通过时序签核。负建立裕量表示最差路径比允许的数据到达时间晚了 6.699 ns，可能在温度/电压/布局变化时采样不可靠；不表示当前屏幕必然立即出错。不能据此直接计算整机可运行频率。

任务02已重新构建：SDRAM C1/C2 为 41.667 MHz/180°，正式报告 SWNS +0.133 ns、STNS 0、HWNS +0.003 ns、HTNS 0。TD 综合阶段仍可能报告加密核内 `Sdr_rd_dout_reg[*].clk` 未驱动；网表核查表明有效 32 位采样已并入 `EG_PHY_PAD`，`ipclk` 接 `u1_init_ref/Sdr_clk`，最终合法化网表不含旧残留寄存器。不得把此分类证据等同于工具日志消失，也不能用 false path 掩盖违例。SDRAM/TF/HDMI 的真实板验收仍需烧录新位流后完成。
