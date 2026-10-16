from pathlib import Path
import shutil
import subprocess

project = Path(__file__).resolve().parents[2]
task = project / "board/task02"
trial = task / "trial_125_timingultra"
trial.mkdir(parents=True, exist_ok=True)
pll = project / "IP/sys_pll.v"
defs = [project / "include/global_def.v", project / "user_source/hdl_source/include/global_def.v"]
al = project / "HX4S20_HDMI_Config.al"
backups = {pll: pll.read_bytes(), al: al.read_bytes(), **{p: p.read_bytes() for p in defs}}
try:
    shutil.copy2(task / "baseline/IP/sys_pll.v", pll)
    for p in defs:
        s = p.read_text(encoding="utf-8").replace("`define\t  SDR_CLK_PERIOD\t\t\t\t24", "`define\t  SDR_CLK_PERIOD\t\t\t\t1000000000/125000000")
        p.write_text(s, encoding="utf-8")
    s = al.read_text(encoding="utf-8").replace("Default_PhysicalDesign_Strategy", "TimingUltra")
    al.write_text(s, encoding="utf-8")
    tcl = (project / "board/task02/build_trial.tcl").read_text(encoding="utf-8").replace("trial_41m", "trial_125_timingultra")
    (task / "build_trial_125_timingultra.tcl").write_text(tcl, encoding="utf-8")
    log = task / "trial_125_timingultra_console.log"
    with log.open("w", encoding="utf-8") as f:
        result = subprocess.run(["td_commands_prompt.exe", "board/task02/build_trial_125_timingultra.tcl"], cwd=project, stdout=f, stderr=subprocess.STDOUT, timeout=900)
    raise SystemExit(result.returncode)
finally:
    for p, data in backups.items():
        p.write_bytes(data)
