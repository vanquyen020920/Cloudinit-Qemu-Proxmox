import os
import subprocess
import datetime

log_file = r"C:\Program Files\Cloudbase Solutions\Cloudbase-Init\log\nvidia-license.log"

def write_log(msg):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("[{}] {}\n".format(datetime.datetime.now(), msg))

nvlts_dir = r"C:\Program Files\NVLTS"
nvlts = os.path.join(nvlts_dir, "nvlts.exe")
config = os.path.join(nvlts_dir, "configs", "vWS.json")

write_log("Start NVIDIA vWS license activation")

if os.path.exists(nvlts):
    if os.path.exists(config):
        cmd = [nvlts, "-g", "-r", "-c", config]
        write_log("Running: {}".format(" ".join(cmd)))

        p = subprocess.Popen(
            cmd,
            cwd=nvlts_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        output, _ = p.communicate()
        write_log(output)
        write_log("nvlts exit code: {}".format(p.returncode))
    else:
        write_log("ERROR: config not found: {}".format(config))
else:
    write_log("ERROR: nvlts.exe not found: {}".format(nvlts))

try:
    p = subprocess.Popen(
        ["nvidia-smi", "-q"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    output, _ = p.communicate()
    write_log(output)
except Exception as e:
    write_log("ERROR running nvidia-smi: {}".format(e))

write_log("Finished NVIDIA vWS license activation")
