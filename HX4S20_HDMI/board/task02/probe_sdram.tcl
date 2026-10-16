set base [file normalize [file join [file dirname [info script]] ../..]]
cd $base
file mkdir board/task02/probe
import_device eagle_s20.db -package EG4S20BG256
open_project HX4S20_HDMI_Config.al -single_run
elaborate -top hx4s20_board_top
read_adc constraints/hx4s20_hdmi_a.adc
optimize_rtl
puts {TASK02_RTL_CONNECTIONS}
report_cells [get_cells {u_app/U3/u2_ram/u2_wrrd/Sdr_rd_dout_reg*}] -connection
report_nets [get_nets {u_app/U3/u2_ram/u2_wrrd/*clk*}] -connection
read_sdc constraints/hx4s20_clocks.sdc
optimize_gate
puts {TASK02_GATE_CONNECTIONS}
report_cells [get_cells {u_app/U3/u2_ram/u2_wrrd/Sdr_rd_dout_reg*}] -connection

export_db board/task02/probe/gate.db
write_verilog board/task02/probe/gate.v
close_project
exit
