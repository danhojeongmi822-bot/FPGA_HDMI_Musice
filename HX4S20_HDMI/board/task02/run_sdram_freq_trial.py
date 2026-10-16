from pathlib import Path
import shutil
import subprocess
import sys
freq = sys.argv[1]
div, cphase1, cphase2, period = {"62.5": (16, 15, 7, 16), "50": (20, 19, 9, 20), "43.478": (23, 22, 11, 23)}[freq]
project = Path(__file__).resolve().parents[2]
task = project / "board/task02"
trial_name = "trial_" + freq.replace('.', 'p')
trial = task / trial_name
trial.mkdir(parents=True, exist_ok=True)
pll = project / "IP/sys_pll.v"
defs = [project / "include/global_def.v", project / "user_source/hdl_source/include/global_def.v"]
al = project / "HX4S20_HDMI_Config.al"
backups = {pll: pll.read_bytes(), al: al.read_bytes(), **{p: p.read_bytes() for p in defs}}
try:
    s = (task / "baseline/IP/sys_pll.v").read_text(encoding="utf-8")
    s = s.replace(".CLKC1_DIV(8)", f".CLKC1_DIV({div})").replace(".CLKC1_CPHASE(7)", f".CLKC1_CPHASE({cphase1})")
    s = s.replace(".CLKC2_DIV(8)", f".CLKC2_DIV({div})").replace(".CLKC2_CPHASE(3)", f".CLKC2_CPHASE({cphase2})")
    pll.write_text(s, encoding="utf-8")
    for p in defs:
        s = p.read_text(encoding="utf-8").replace("`define\t  SDR_CLK_PERIOD\t\t\t\t24", f"`define\t  SDR_CLK_PERIOD\t\t\t\t{period}")
        p.write_text(s, encoding="utf-8")
    tcl = (project / "board/task02/build_trial.tcl").read_text(encoding="utf-8").replace("trial_41m", trial_name)
    (task / f"build_{trial_name}.tcl").write_text(tcl, encoding="utf-8")
    log = task / f"{trial_name}_console.log"
    with log.open("w", encoding="utf-8") as f:
        result = subprocess.run(["td_commands_prompt.exe", f"board/task02/build_{trial_name}.tcl"], cwd=project, stdout=f, stderr=subprocess.STDOUT, timeout=900)
    raise SystemExit(result.returncode)
finally:
    for p, data in backups.items():
        p.write_bytes(data)
