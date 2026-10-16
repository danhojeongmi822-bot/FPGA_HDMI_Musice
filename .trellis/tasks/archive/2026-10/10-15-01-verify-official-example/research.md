# 验证证据与研究入口

先读 docs/对话历史整理.md 和 docs/上板现象对照.md，区分代码预期与用户初测。

源码证据：board/hx4s20_board_top.v 说明位选与复位释放；top_tf_hdmi_audio.v 的 seg_data_0～4 空白、seg_data_5 接状态码；SD/bmp_read.v 的状态码与物理扇区扫描说明显示 2 的含义。PLL 配置与既有修复见 .trellis/spec/fpga/clock-reset.md 及 上板前核查结果.md。

报告证据：board/regression_results.json、board/pin_verification.json、build_hx4s20/route_timing.rpt、route_timing_status.rpt、route.area 及位流。原始复制清单见 board/migration_manifest.json，迁移核查见 board/migration_verification.json。

实板证据：2026-10-15 用户消息，未由代理测量；没有逐项拍照/测量、实际下载文件哈希及长稳时长，不补造数据。后续优化从当前基线出发，需另立任务。
