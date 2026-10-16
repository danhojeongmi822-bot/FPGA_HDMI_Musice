# 初步研究

原始最差路径来自SDRAM硬核DQ到综合PAD，半周期预算4ns；Map Macro后出现读寄存器clk未驱动。根因尚待网表确认。官方同版lab6包装层同样实例化EG_PHY_SDRAM_2M_32。基线保存于HX4S20_HDMI/board/task02/baseline/。

正式根因确认：原始最差路径来自SDRAM硬核DQ到综合PAD，125MHz移相读路径数据延迟6.453ns、时钟偏差4.306ns，报告-6.699ns；写路径报告-2.842ns。官方同版lab6包装层同样实例化EG_PHY_SDRAM_2M_32。

TD 6.2.168116网表追踪显示，有效32位输入采样被并入EG_PHY_PAD，IN_DFFMODE("FF")、INPCLKMUX("CLK")、ipclk=u1_init_ref/Sdr_clk；Map Macro日志中的Sdr_rd_dout_reg[*].clk=0是无输出、被keep保留的旧单元，最终legalize后不在gate.v中。不能给这些寄存器硬接时钟，也不能修改加密核主体。

修复试验将SDRAM C1/C2改为41.667MHz、24ns周期、180度相差12ns；mem/TF读写应答增加两级同步。正式route STA为SWNS +0.133ns、STNS 0、HWNS +0.003ns、HTNS 0，覆盖99.64%；位流哈希写入result.md与sdram_mapping_verification.json。综合日志仍列出原始告警文本，验证脚本只分类最终物理网表，不能消除工具消息。

根因类别：跨层时序预算不足与CDC握手契约缺失（D/E）。预防：改变PLL或周期时同步两份global_def、刷新计数和注释；跨域电平握手必须有接收端两级同步；STA同时查看最差路径和跨域组；最终必须实板记录。

## 最优方案频率试验（2026-10-16）

当前正式工程的 C1/C2=41.666667 MHz（DIV24，0°/180°）是已验证通过的最高可接受候选：SWNS +0.133 ns。125 MHz 原方案和 TimingUltra 均为 -6.699 ns；C2 单独加 BUFG 为 -6.826 ns；62.5 MHz 为 -2.699 ns；50 MHz 为 -0.699 ns；43.478 MHz 的奇数分频报告出现异常时钟分组，未采用。详细比较和后续厂商 SIP 约束路线见 `docs/任务02_SDRAM最优方案研究.md`。

器件数据手册给出的片上 SDR SDRAM 最高规格为 200 MHz，说明本次降频是当前 SIP/加密控制器/约束组合下的时序收敛措施，不是器件频率上限。恢复 50 或 125 MHz 应先获取安路对 `EG_PHY_SDRAM_2M_32` 的专用延迟补偿、PLL 相位和约束建议，再重跑全 STA 与实板验证。
