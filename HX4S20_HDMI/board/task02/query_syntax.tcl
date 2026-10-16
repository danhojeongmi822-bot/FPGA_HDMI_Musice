foreach cmd {get_property set_property remove_cell get_pins} {
 puts "COMMAND $cmd"
 catch {$cmd} result
 puts $result
}
exit
