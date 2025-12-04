Here’s a focused `README.md` you can drop into your `SO101_env` folder to guide you during the hackathon. Adjust paths/names as needed for your specific setup.

***

# SO‑101 Hackathon README

## 1. Daily startup checklist

Every new terminal session:

```bash
# 1. Enable conda/mamba in this shell (if not already active)
source ~/miniforge3/bin/activate

# 2. Activate the LeRobot environment
conda activate lerobot

# 3. Go to this project folder
cd ~/Desktop/SO101_env/Lerobot_script
```

Quick sanity check:

```bash
python -c "import lerobot; print(lerobot.__version__)"
```

If it prints a version (e.g. `0.4.2`), the environment is ready.

***

## 2. Environment recap

What is installed in `lerobot` conda env:

- Python 3.10  
- `lerobot` (core LeRobot library)  
- `ffmpeg` (video encode/decode for datasets, demos, logging)  
- PyTorch + other ML dependencies

If you ever completely lose the environment on a hackathon machine, recreate it with roughly:

```bash
conda create -y -n lerobot python=3.10
conda activate lerobot
conda install ffmpeg -c conda-forge
pip install lerobot
```

(Only if you really have to; ideally the hackathon machine will already be prepared.)

***

## 3. Basic workflow with SO‑101

The typical LeRobot + SO‑101 loop is:

1. **Connect robot hardware**
   - Plug SO‑101 controller into the machine (usually USB‑C / USB‑A).
   - Turn on power, ensure emergency stop is released.
   - Confirm the device appears (e.g. as `/dev/tty*` on Linux, COM port on Windows).

2. **Teleop / record demonstrations**
   - Use the provided LeRobot scripts or SO‑101 helper tools to move the arm by hand or joystick and record trajectories.
   - This produces a dataset (typically a folder with episodes, video + state/action arrays).

3. **Inspect dataset**
   - Load dataset with LeRobot (small Python script or existing tool).
   - Check: number of episodes, episode length, observation shapes, video playback.

4. **Train a policy**
   - Run the training script with the dataset path and config (BC, diffusion policy, etc.).
   - Watch logs/metrics to see if training is progressing.

5. **Deploy/run the policy**
   - Use a control script to run the trained policy on the real SO‑101.
   - Monitor behaviour and adjust (safety limits, speeds, gains, camera framing, etc.).

Try to keep each of these steps **small and testable** so you can debug quickly during the event.

***

## 4. Useful local scripts to have ready

Create a few simple scripts in this folder to speed up debugging on any machine.

### 4.1 Check PyTorch and device

`check_torch_device.py`:

```python
import torch

print("Torch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("CUDA device:", torch.cuda.get_device_name(0))
else:
    print("Running on CPU")
```

Run:

```bash
python check_torch_device.py
```

Use this immediately on any new machine to know if you have a GPU.

***

### 4.2 Check LeRobot and ffmpeg

`check_lerobot_ffmpeg.py`:

```python
import subprocess
import lerobot

print("LeRobot version:", lerobot.__version__)

try:
    out = subprocess.check_output(["ffmpeg", "-version"], stderr=subprocess.STDOUT)
    first_line = out.decode("utf-8").splitlines()[0]
    print("ffmpeg:", first_line)
except Exception as e:
    print("ffmpeg check failed:", e)
```

Run:

```bash
python check_lerobot_ffmpeg.py
```

If this fails, fix ffmpeg **before** recording anything.

***

## 5. Working with code during the hackathon

Recommended mental model:

- **Editor (Cursor/VS Code)**: write and organize Python files and configs.
- **Terminal**: activate the `lerobot` env and run those scripts.

Basic pattern:

1. Open editor on your project folder (`SO101_env` or similar).
2. Create or edit a script (e.g. `record_demos.py`, `train_policy.py`, `run_policy.py`).
3. In Terminal (env active, in same folder):

   ```bash
   python record_demos.py
   ```

Use clear filenames and keep everything in this folder so you can zip it or push to git quickly.

***

## 6. Time‑pressure survival tips

- **Automate the startup steps**:  
  Make sure you can, from memory, do:

  ```bash
  source ~/miniforge3/bin/activate
  conda activate lerobot
  cd /path/to/project
  python check_lerobot_ffmpeg.py
  ```

- **Log everything**:
  - Save configs (YAML/JSON), command lines, and notes inside this folder.
  - Keep a `NOTES.md` with: dataset path(s), training commands, best checkpoints.

- **Minimize surprises**:
  - Before the hackathon, test:
    - Importing `lerobot` on your own machine.
    - Running a trivial script that loads a dummy or example dataset (if you have one).
    - At least one training command on any machine with a GPU, if you get access.

***

## 7. What to review conceptually

Without the robot in front of you, focus on understanding:

- The *pipeline*: demo → dataset → model training → deployment.
- What a **dataset** looks like (episodes, observations, actions, videos).
- How to:
  - Activate the environment quickly.
  - Run scripts with arguments.
  - Inspect errors and logs.

You don’t need to master every model; being fast and reliable with the **tooling** and **basic scripts** will already put you in a strong position.

***


