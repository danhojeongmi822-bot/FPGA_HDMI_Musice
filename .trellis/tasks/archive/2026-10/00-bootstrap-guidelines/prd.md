# 任务 00：完成 FPGA 工程规范初始化

## 目标与边界

用户要求完成第 0 个 Trellis 任务。把初始化时的 Web fullstack 空模板替换成真实 Verilog/安路 TD 规范；模板作为历史参考移存本任务。该任务不修改业务 RTL，也不解决时序违例。

## 验收

- [x] 根据 hx4s20_board_top、top、BMP 读取与现有测试建立架构规范。
- [x] 明确 PLL/复位/像素/FIFO/板卡接口契约与真实示例。
- [x] 明确验证命令、现有 STA 风险和用户初测的证据边界。
- [x] 增加规范索引、迁移及会话记录约定，无未填写模板留在活动规范树。

## 结果

规范位于 .trellis/spec/fpga/。原 backend/frontend 模板保存在本任务 template-reference/。使用 trellis-spec-bootstrap 单人完成，未派生子代理。按用户要求归档，使用 --no-commit；Git 初次提交另行审核，不视作规范尚未完成。
