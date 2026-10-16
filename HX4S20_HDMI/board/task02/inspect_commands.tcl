foreach cmd {export_verilog write_verilog export_db import_db report_cells report_nets optimize_gate} {
 puts "COMMAND $cmd"
 catch {$cmd -help} result
 puts $result
}
exit
