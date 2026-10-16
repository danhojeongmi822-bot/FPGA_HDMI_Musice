> 路径约定：以下源码、素材、构建产物路径均相对 HX4S20_HDMI/；Trellis 与 docs 路径相对工作区根。当前 TD 入口 HX4S20_HDMI/HX4S20_HDMI_Config.al。

# 时钟、复位与流接口

## 实际时钟

|来源|输出|用途|
|---|---|---|
|板载时钟|50 MHz，R7|PLL 输入|
|sys_pll C0|100 MHz，0°|TF、写 FIFO|
|sys_pll C1|41.667 MHz，0°|SDRAM 逻辑|
|sys_pll C2|41.667 MHz，180°|SDRAM 移相时钟，与 C1 差 12 ns|
|video_pll C0|25 MHz|像素，800×525 总时序约 59.52 Hz|
|video_pll C1|125 MHz|HDMI 5 倍串行时钟，ODDR 双沿|
|audio PLL C2|12.295082 MHz|音频主时钟，采样约 48027.66 Hz|

音频 PLL C0 75 MHz 用于反馈，C1 375 MHz 未用于业务。不能把注释中的标称频率当作精确频率。

## 复位契约

真实实现见 top_tf_hdmi_audio.v 与 board/hx4s20_board_top.v：

```verilog
wire rst_all = ~rst_n | ~sys_pll_lock | ~video_pll_lock | ~audio_pll_lock;
reset_release reset_sd(sd_card_clk, rst_all, rst_sd);
```

reset_release 异步置位、本域稳定运行 16 个时钟沿后释放；各域分别实例化，丢锁重新复位。I2S_receiver.v 和视频延迟寄存器使用各自复位。不得直接将未锁定 PLL 的输出当作已稳定时钟，也不能以复位同步替代完整 CDC 分析。对应验证 board/tests/tb_reset.v。

## 像素与 FIFO 契约

video_rgb_to_axis_640x480.v 首个有效像素计数后应为 1，第 640 个有效像素产生 TLAST，帧首 SOF。board/tests/tb_video_axis.v 对像素和标志逐项断言。FIFO 真实占用计数为 9 位，向控制器 10 位接口显式补零；保持顶层帧地址和长度位宽一致。AXIS ready 背压尚未完整验证，不得宣称任意背压下已通过。

约束 constraints/hx4s20_clocks.sdc 目前仅输入 create_clock 和 derive_clocks，尚不构成完整 IO/CDC 时序签核。严禁用全局 false path 或随意改 PLL 相位掩盖违例。
