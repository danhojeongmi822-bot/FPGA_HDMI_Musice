> 路径约定：以下源码、素材、构建产物路径均相对 HX4S20_HDMI/；Trellis 与 docs 路径相对工作区根。当前 TD 入口 HX4S20_HDMI/HX4S20_HDMI_Config.al。

# 架构与代码组织

工程入口 HX4S20_HDMI/HX4S20_HDMI_Config.al，器件 EG4S20BG256，顶层 board/hx4s20_board_top.v 的 hx4s20_board_top，内部实例 top u_app 来自 top_tf_hdmi_audio.v。TD 版本 6.2.168116。用户板卡名称 HX42S20，以《HX4S20开发板手册-HDL版2410》及实际引脚对应为准。

图片数据路径：TF SPI → SD/bmp_read.v → FIFO → SD/sdram.v → FIFO → video_rgb_to_axis_640x480.v → HDMI 加密核 → ODDR/LVDS33 → HDMI A。音频来自 hdmi_audio_tone_i2s_64fs.v，经过 I2S_receiver.v 接入 HDMI，不具备 TF 音频文件解码能力。

- board/：板级适配、构建脚本、单元测试和验证记录。
- constraints/：ADC 引脚和 SDC 时钟。
- SD/：卡控制、BMP 和当前使用的 SDRAM 控制器。
- IP/、hdmi1.4b_transmitter_core/、user_source/：PLL/FIFO/加密核及兼容头文件。
- assets/tf/：可直接用于回归的四张 BMP。
- build_hx4s20/：保留的位流与综合、布线、时序报告；属于可追溯实验产物。
- spec/：迁入的历史核查文档；新的开发规范以 .trellis/spec/ 为准。

## 源码约束

.al 中只能注册 SD/sdram.v；IP/sdram.v 同名模块保留磁盘参考但不得同时加入编译。修改源引用必须核查 AutoExcluded 和顶层，不能仅靠磁盘存在判断已参与构建。不要改写加密控制器主体。include/global_def.v 与 user_source/hdl_source/include/global_def.v 必须保持同步。

TD 的 .al 使用 UsedInP&R 裸 &；Python XML 读取参照 board/verify_pin_report.py，解析前替换为 UsedInP&amp;R，不随意重排工程格式。迁移只改变根 Project Path，源文件使用相对路径。构建脚本 board/build_project.tcl 已按自身位置定位根目录。
