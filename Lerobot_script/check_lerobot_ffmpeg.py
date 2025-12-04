import subprocess
import lerobot

print("LeRobot version:", lerobot.__version__)

try:
    out = subprocess.check_output(["ffmpeg", "-version"], stderr=subprocess.STDOUT)
    first_line = out.decode("utf-8").splitlines()[0]
    print("ffmpeg:", first_line)
except Exception as e:
    print("ffmpeg check failed:", e)
