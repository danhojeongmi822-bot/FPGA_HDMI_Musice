from pathlib import Path
import subprocess
import tempfile
import shutil
import json
import sys
base=Path(__file__).resolve().parent.parent
compiler=Path('C:/iverilog/bin/iverilog.exe')
runtime=compiler.with_name('vvp.exe')
results=[]
def run(name, files, args=()):
    output=base/'board/tests'/(name+'.vvp')
    subprocess.run([str(compiler),'-g2012','-s',name,'-o',str(output),*files],cwd=base,check=True,capture_output=True,text=True)
    result=subprocess.run([str(runtime),str(output),*args],cwd=base,capture_output=True,text=True)
    print(result.stdout,end='')
    results.append({'test':name,'arguments':list(args),'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    if result.returncode: raise RuntimeError(name+' failed')
run('tb_video_axis',['board/tests/tb_video_axis.v','video_rgb_to_axis_640x480.v'])
run('tb_audio',['board/tests/tb_audio.v','hdmi_audio_tone_i2s_64fs.v','I2S_receiver.v'])
run('tb_reset',['board/tests/tb_reset.v','board/hx4s20_board_top.v'])
run('tb_frame_ack',['board/tests/tb_frame_ack.v','SD/frame_read_write.v','SD/frame_fifo_read.v','SD/frame_fifo_write.v'])
images=Path(sys.argv[1]) if len(sys.argv)>1 else base/'assets/tf'
with tempfile.TemporaryDirectory(prefix='hx4s20_') as temp:
    for index in range(1,5):
        image=images/(str(index).zfill(3)+'.bmp')
        target=Path(temp)/'image.bmp'
        shutil.copyfile(image,target)
        run('tb_bmp',['board/tests/tb_bmp.v','SD/bmp_read.v'],['+BMP='+target.as_posix()])
        results[-1]['source_image']=str(image)
(base/'board/regression_results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('All targeted regressions passed. Protected IP and physical board are outside this simulation.')
