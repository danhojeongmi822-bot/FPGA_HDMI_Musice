set base [file normalize [file join [file dirname [info script]] ..]]
cd $base
file mkdir build_hx4s20
import_device eagle_s20.db -package EG4S20BG256
open_project HX4S20_HDMI_Config.al -single_run
elaborate -top hx4s20_board_top
read_adc constraints/hx4s20_hdmi_a.adc
optimize_rtl
read_sdc constraints/hx4s20_clocks.sdc
optimize_gate
legalize_phy_inst
read_sdc constraints/hx4s20_clocks.sdc
export_db build_hx4s20/gate.db
report_area -file build_hx4s20/gate.area
puts {HX4S20_SYNTHESIS_FINISHED}
place
report_area -io_info -file build_hx4s20/place.area
route
export_db build_hx4s20/route.db
report_area -io_info -file build_hx4s20/route.area
update_timing -mode final
report_timing_summary -file build_hx4s20/route_timing.rpt
report_timing_status -file build_hx4s20/route_timing_status.rpt
bitgen -bit build_hx4s20/HX4S20_HDMI_Config.bit
puts {HX4S20_BITGEN_FINISHED}
close_project
exit
