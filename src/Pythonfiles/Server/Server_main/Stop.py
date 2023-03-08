import subprocess

def stop():
    # use the subprocess module to run the "taskkill" command to stop the batch file
    subprocess.call('taskkill /f /im java.exe', shell=True)