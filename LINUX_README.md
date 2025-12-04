Below is a Linux‑specific `LINUX-README.md` you can drop into your repo. It assumes an Ubuntu‑like environment and a fresh user account, and it mirrors the flow you already used on macOS.[1][2]

***

# LINUX-README – SO‑101 + LeRobot

This file is for quickly setting up and using LeRobot with SO‑101 on a **Linux** machine during the hackathon.

***

## 1. One‑time setup on a new Linux machine

### 1.1 Install Miniforge (conda-forge Python distribution)

In a fresh terminal:

```bash
# Go to home directory
cd ~

# Download Miniforge installer for Linux (x86_64 / AMD64)
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" -O Miniforge3.sh

# Run the installer (interactive)
bash Miniforge3.sh
```

During installation:

- Accept the license.
- Accept the default install path (e.g. `~/miniforge3`).
- Say **yes** when asked to initialize conda/mamba for your shell.[3][4]

Then **close the terminal** and open a **new** one so shell initialization takes effect.

***

### 1.2 Verify conda works

In a new terminal:

```bash
conda --version
```

If `conda` is not found, manually source Miniforge:

```bash
source ~/miniforge3/bin/activate
conda --version
```

You should see a conda version printed.

***

### 1.3 Create the `lerobot` environment

```bash
conda create -y -n lerobot python=3.10
conda activate lerobot
```

You will need to run `conda activate lerobot` every time you open a new terminal and want to work with LeRobot.[5][1]

***

### 1.4 Install `ffmpeg` in the environment

Still in `(lerobot)`:

```bash
conda install -y -c conda-forge "ffmpeg>=7.0"
```

This typically installs `ffmpeg 7.X` compiled with `libsvtav1` on Linux.[6][1]

Verify:

```bash
ffmpeg -version | head -n 1
ffmpeg -encoders | grep svt
```

If `libsvtav1` is missing and you need it, you can instead pin a specific version:

```bash
conda install ffmpeg=7.1.1 -c conda-forge
```

***

### 1.5 Install LeRobot

In the same `(lerobot)` environment:

```bash
pip install lerobot
```

Check it imports correctly:

```bash
python -c "import lerobot; print(lerobot.__version__)"
```

If you need the **latest dev version** or specific extras, you can instead:

```bash
# Example: install directly from GitHub with pi extras (if required by the hackathon)
pip install "lerobot[all]@git+https://github.com/huggingface/lerobot.git"
```

See the LeRobot installation docs for tags like `[all]`, `[feetech]`, etc.[7][1]

***

## 2. Per‑session startup checklist (every new terminal)

Any time you open a new terminal on Linux:

```bash
# 1. Make sure conda is available
source ~/miniforge3/bin/activate    # only if `conda` is not found

# 2. Activate the LeRobot env
conda activate lerobot

# 3. Go to your project folder
cd ~/SO101_env             # or wherever you cloned your project
```

Quick sanity checks:

```bash
python -c "import lerobot; print(lerobot.__version__)"
ffmpeg -version | head -n 1
```

***

## 3. Project layout on Linux

Recommended simple structure under your $HOME:

```text
~/SO101_env/
  LINUX-README.md
  NOTES.md
  scripts/
    check_torch_device.py
    check_lerobot_ffmpeg.py
    record_demos.py
    train_policy.py
    run_policy.py
  data/
    demos/
    datasets/
  models/
    checkpoints/
```

Create it:

```bash
mkdir -p ~/SO101_env/scripts ~/SO101_env/data/demos ~/SO101_env/models/checkpoints
cd ~/SO101_env
```

You can then open this folder in your editor (VS Code / Cursor) and run scripts from a terminal in the same directory.

***

## 4. Useful scripts on Linux

### 4.1 Check PyTorch and GPU

`~/SO101_env/scripts/check_torch_device.py`:

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
cd ~/SO101_env
conda activate lerobot
python scripts/check_torch_device.py
```

This tells you whether the hackathon machine sees a GPU and which one.[8]

***

### 4.2 Check LeRobot and ffmpeg

`~/SO101_env/scripts/check_lerobot_ffmpeg.py`:

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
cd ~/SO101_env
conda activate lerobot
python scripts/check_lerobot_ffmpeg.py
```

If this fails, fix `ffmpeg` before recording datasets.[9][1]

***

## 5. SO‑101 specifics on Linux

Once the base environment works, you’ll connect the SO‑101.

### 5.1 USB / serial permissions

When you plug in the SO‑101 controller, it should appear as `/dev/ttyACM0` or `/dev/ttyUSB0` etc.[10][9]

Check:

```bash
ls /dev/ttyACM* /dev/ttyUSB* 2>/dev/null
```

If you get a permission error when trying to connect, temporarily relax permissions (for hackathon dev use only):

```bash
sudo chmod 666 /dev/ttyACM0
# or, if your device is /dev/ttyUSB0:
sudo chmod 666 /dev/ttyUSB0
```

(Some setups might use `dialout` group membership instead, but `chmod` is the quick hackathon‑friendly way.)

***

### 5.2 Follow SO‑101 LeRobot docs

With environment and permissions ready, follow the official SO‑101 docs for:

- Motor setup (`lerobot-setup-motors` for leader/follower).  
- Calibration (`lerobot-calibrate`).  
- Recording demonstrations and running policies.[11][12][10]

Keep the key commands you use (with arguments and ports) copied into `NOTES.md` for quick reuse.

***

## 6. Common recovery patterns on Linux

### 6.1 If `conda` stops working

- Try:

  ```bash
  source ~/miniforge3/bin/activate
  conda --version
  ```

- If that fails, check Miniforge install dir:

  ```bash
  ls ~/miniforge3
  ```

If the folder is gone/corrupted, reinstall Miniforge and recreate the `lerobot` env as in section 1.[13][4]

***

### 6.2 If `lerobot` import fails

Re‑install into the current env:

```bash
conda activate lerobot
pip install --upgrade --force-reinstall lerobot
python -c "import lerobot; print(lerobot.__version__)"
```

***

### 6.3 If `ffmpeg` is missing or lacks `libsvtav1`

Reinstall from conda‑forge:

```bash
conda activate lerobot
conda install -y -c conda-forge "ffmpeg>=7.0"
# or explicitly:
conda install ffmpeg=7.1.1 -c conda-forge
ffmpeg -encoders | grep svt
```


***

## 7. Minimal mental checklist for the hackathon

On any Linux box, you should be able to do, from memory:

```bash
# 1. Ensure conda + env
source ~/miniforge3/bin/activate      # if needed
conda activate lerobot

# 2. Go to project
cd ~/SO101_env

# 3. Quick checks
python scripts/check_lerobot_ffmpeg.py
python scripts/check_torch_device.py

# 4. Work with SO-101
# (using your recorded commands / scripts from the official SO-101 docs)
```

If you have this `LINUX-README.md` and `NOTES.md` beside your scripts, you will have a clear path from bare Linux machine → working SO‑101 + LeRobot environment under time pressure.

[1](https://huggingface.co/docs/lerobot/en/installation)
[2](https://conda-forge.org/download/)
[3](https://docs.dkist.nso.edu/projects/python-tools/en/v1.11.0/installation.html)
[4](https://github.com/conda-forge/miniforge)
[5](https://maegant.github.io/ECE4560/assignment2-so101/)
[6](https://docs.trossenrobotics.com/trossen_arm/v1.4/tutorials/lerobot/setup.html)
[7](https://github.com/huggingface/lerobot)
[8](https://aifitlab.com/blogs/tech-blogs/lerobot-project-runtime-environment-setup-guide)
[9](https://wiki.seeedstudio.com/lerobot_so100m/)
[10](https://openelab.io/de/blogs/seeed-studio/build-your-own-so-101-robot)
[11](https://huggingface.co/docs/lerobot/en/so101)
[12](https://phospho.mintlify.app/so-101/quickstart)
[13](https://gist.github.com/elejke/3437be39478c66a3efac26700cb14334)
[14](https://ai.robotis.com/omx/setup_guide_lerobot.html)
[15](https://partabot-1.gitbook.io/partabot/so-arm101/assembled-kit)
[16](https://www.kamenski.me/articles/robotics-made-simple-playing-with-lerobot-and-so-101)
[17](https://www.waveshare.com/wiki/SO-ARM100/101_Install_Lerobot_Environment)
[18](https://dragons.readthedocs.io/projects/recipe-system-users-manual/en/v3.2.0/install.html)
[19](https://www.ncnynl.com/ros2docs/en/aloha/training/lerobot_guide.html)
[20](https://www.hpc.cmc.osaka-u.ac.jp/en/system/manual/squid-use/miniforge/)