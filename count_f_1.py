import subprocess

def read_audit():
    cmd = "aureport -f -i"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    res = p.stdout.read().decode()
    return res

print(read_audit())