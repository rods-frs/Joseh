import subprocess
program = "github desktop"
name_command = ["flatpak", "search", "--columns=name", program]
id_command = ["flatpak", "search", "--columns=application", program]
try:
    result1 = subprocess.run(name_command,text=True,capture_output=True,check=True)
    result2 = subprocess.run(id_command,text=True, capture_output=True,check=True)

except Exception as e:
    print(f"stderr: {getattr(e, 'stderr', 'N/A')}")
print(result1.stderr)

result2_lines = result2.stdout.splitlines()
idx = -1
for line in result1.stdout.splitlines():
    idx += 1
    if program in line.lower():
        print(result2_lines[idx])
