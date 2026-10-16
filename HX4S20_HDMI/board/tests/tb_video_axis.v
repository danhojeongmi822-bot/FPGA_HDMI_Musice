`timescale 1ns/1ps
module tb_video_axis;
reg clk=0, rst=1, vs=0, de=0;
reg [23:0] rgb=0;
wire user, valid, last;
wire [23:0] data;
integer frame, row, x, users=0, lasts=0, pixels=0;
always #20 clk=~clk;
video_rgb_to_axis_640x480 dut(clk,rst,vs,de,rgb,user,valid,last,data);
initial begin
 repeat(3) @(negedge clk); rst=0;
 for(frame=0;frame<2;frame=frame+1) begin
  vs=1; repeat(3) @(negedge clk); vs=0; repeat(3) @(negedge clk);
  for(row=0;row<3;row=row+1) begin
   for(x=0;x<640;x=x+1) begin
    de=1; rgb=frame*10000+row*640+x;
    @(posedge clk); #1;
    if(!valid || data!==rgb) $fatal(1,"pixel mismatch");
    if(last !== (x==639)) $fatal(1,"TLAST mismatch at pixel %0d (expected x=639)",x);
    if(user !== (row==0 && x==0)) $fatal(1,"SOF mismatch");
    pixels=pixels+1; if(last) lasts=lasts+1; if(user) users=users+1;
    @(negedge clk);
   end
   de=0; repeat(5) @(negedge clk);
  end
 end
 if(pixels!=3840 || lasts!=6 || users!=2) $fatal(1,"frame counts mismatch");
 $display("PASS video: 3840 pixels, 6 TLAST, 2 SOF"); $finish;
end
endmodule
