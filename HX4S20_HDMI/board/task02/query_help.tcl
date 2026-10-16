foreach cmd {set_attribute remove_attribute remove_cell remove_cells delete_cell get_pins get_property set_property set_clock_net report_timing report_timing_summary optimize_gate set_option} {
 puts "COMMAND $cmd"
 catch {$cmd -help} result
 puts $result
}
exit
