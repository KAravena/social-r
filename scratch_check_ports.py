import subprocess

out = subprocess.check_output(['wmic', 'process', 'where', 'caption="deno.exe"', 'get', 'ProcessId,CommandLine'], text=True)
print(out)
