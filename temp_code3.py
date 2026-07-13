import subprocess
program = "discord"
name_command = ["flatpak", "list", "--app","--columns=application"]
try:
    result1 = subprocess.run(name_command,text=True,capture_output=True,check=True)
except Exception as e:
    print(f"stderr: {getattr(e, 'stderr', 'N/A')}")
print(result1.stderr)

idx = -1
for line in result1.stdout.splitlines():
    idx += 1
    if program in line.lower():
        print(line)
        execution_command = ["flatpak", "run", line]
        subprocess.Popen(execution_command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)