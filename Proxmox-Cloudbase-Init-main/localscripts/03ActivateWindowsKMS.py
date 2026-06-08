import os
import subprocess
import datetime

log_file = r"C:\Program Files\Cloudbase Solutions\Cloudbase-Init\log\windows-kms-activation.log"

kms_key = "M7XTQ-FN8P6-TTKYV-9D4CC-J462D"
kms_server = "103.147.122.144"

activate_cmd_path = r"C:\ProgramData\ActivateWindowsKMS.cmd"
slmgr = r"C:\Windows\System32\slmgr.vbs"
cscript = r"C:\Windows\System32\cscript.exe"

def write_log(msg):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("[{}] {}\n".format(datetime.datetime.now(), msg))

def run_cmd(cmd):
    write_log("Running: {}".format(" ".join(cmd)))
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    output, _ = p.communicate()
    write_log(output)
    write_log("Exit code: {}".format(p.returncode))
    return p.returncode

write_log("Start Windows KMS activation")

# Create reusable activation CMD
cmd_content = r'''@echo off
set LOG=C:\ProgramData\ActivateWindowsKMS.log
echo [%date% %time%] Start Windows KMS activation >> "%LOG%"
cscript //nologo C:\Windows\System32\slmgr.vbs -ipk M7XTQ-FN8P6-TTKYV-9D4CC-J462D >> "%LOG%" 2>&1
cscript //nologo C:\Windows\System32\slmgr.vbs -skms 103.147.122.144 >> "%LOG%" 2>&1
cscript //nologo C:\Windows\System32\slmgr.vbs -ato >> "%LOG%" 2>&1
cscript //nologo C:\Windows\System32\slmgr.vbs -dlv >> "%LOG%" 2>&1
echo [%date% %time%] Finished Windows KMS activation >> "%LOG%"
'''

with open(activate_cmd_path, "w", encoding="utf-8") as f:
    f.write(cmd_content)

write_log("Created activation CMD: {}".format(activate_cmd_path))

# Run activation now
run_cmd([cscript, "//nologo", slmgr, "-ipk", kms_key])
run_cmd([cscript, "//nologo", slmgr, "-skms", kms_server])
run_cmd([cscript, "//nologo", slmgr, "-ato"])
run_cmd([cscript, "//nologo", slmgr, "-dlv"])

# Create scheduled task to run every 180 days as SYSTEM
task_name = "Activate Windows KMS Every 180 Days"

run_cmd([
    r"C:\Windows\System32\schtasks.exe",
    "/Create",
    "/TN", task_name,
    "/TR", activate_cmd_path,
    "/SC", "DAILY",
    "/MO", "180",
    "/RU", "SYSTEM",
    "/RL", "HIGHEST",
    "/F"
])

write_log("Finished Windows KMS activation setup")
