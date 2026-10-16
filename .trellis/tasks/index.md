# Trellis 任务索引

|编号|任务|阶段状态|记录|
|---|---|---|---|
|00|FPGA 工程规范初始化|完成|[需求与结果](archive/2026-10/00-bootstrap-guidelines/prd.md)|
|01|验证官方例程|基本功能初步验证阶段完成，遗留问题保留|[任务需求](archive/2026-10/10-15-01-verify-official-example/prd.md) · [结果](archive/2026-10/10-15-01-verify-official-example/result.md)|
|02|修复SDRAM时序与读数据时钟告警|当前约束下STA与仿真通过，实板待验收|[任务需求](10-16-02-fix-sdram-timing/prd.md) · [结果](10-16-02-fix-sdram-timing/result.md)|

第 01 任务还保存了本次工程迁移和对话整理。后续基于当前代码优化时另建任务，不能将本次阶段完成理解为 SDRAM 时序及整机长期稳定性验收通过。

- [对话历史](../../docs/对话历史整理.md)
- [上板现象对照](../../docs/上板现象对照.md)
- [cheng 会话索引](../workspace/cheng/index.md)

当前工程目录为 HX4S20_HDMI/；工作区一级保留 Trellis 与工程说明，任务01已追加此次目录修正。

- [每个任务的改动与效果说明](../../任务记录/README.md)
