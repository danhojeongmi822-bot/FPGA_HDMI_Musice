set base [file normalize [file join [file dirname [info script]] ../..]]
cd $base
file mkdir board/task02/trial_41m
import_device eagle_s20.db -package EG4S20BG256
open_project HX4S20_HDMI_Config.al -single_run
elaborate -top hx4s20_board_top
read_adc constraints/hx4s20_hdmi_a.adc
optimize_rtl
read_sdc constraints/hx4s20_clocks.sdc
optimize_gate
legalize_phy_inst
read_sdc constraints/hx4s20_clocks.sdc
write_verilog board/task02/trial_41m/gate.v
export_db board/task02/trial_41m/gate.db
place
route
export_db board/task02/trial_41m/route.db
report_area -io_info -file board/task02/trial_41m/route.area
update_timing -mode final
report_timing_summary -file board/task02/trial_41m/route_timing.rpt
report_timing_status -file board/task02/trial_41m/route_timing_status.rpt
bitgen -bit board/task02/trial_41m/HX4S20_HDMI_Config.bit
close_project
exit
