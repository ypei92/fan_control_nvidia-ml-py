# Python-based NVIDIA GPU Fan Controller
This repository implements a pure Python-based fan speed controller for NVIDIA GPUs.

## Motivation
While experimenting with NVIDIA vGPU on Proxmox VE, a popular Debian-based hypervisor,
I encountered an issue: despite installing the NVIDIA drivers,
I couldn't easily control the fan speed.
My graphics card remained at 45°C with dead-still fan.
After extensive research, I found that most solutions required additional packages
like nvidia-xconfig and nvidia-settings, which are not included in the vGPU driver.
Moreover, I prefer to keep the Proxmox VE base operating system as clean as possible.

Eventually, I discovered the nvidia-ml-py Python package,
which provides convenient interfaces to control fan speed.
This repository leverages **nvidia-ml-py** to implement a fan speed controller,
with customizable fan curve points defined under the `profiles/` directory.

## Quick Start
1. Clone the repository to $HOME
```
git clone https://github.com/ypei92/fan_control_nvidia-ml-py.git $HOME/.fan_control_nvidia-ml-py
```
2. Setup dependencies
```
# Setup Python virtual environment (e.g. Python venv, Conda, etc)
cd .fan_control_nvidia-ml-py
python -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install
```

3. Execute program
```
python src/main.py
```
4. Customization with command line options
```
# Arg options
# -p --profile           path/to/your/profile; Default to $HOME/.fan_control_nvidia-ml-py/profiles/default.yml
# -i --control-interval  Fan control interval in seconds; Default to 1 seconds
# -l --log-level         Log level to $HOME/.fan_control_nvidia-ml-py/logs/fan_speed.log; Default to INFO

python src/main.py --profile ~/.fan_control_nvidia-ml-py/profiles/default.yml --control-interval 1 --log-level INFO
```

## Run as systemd.service
1. Modify the service template at `scripts/nvidia-gpu-fan-control.service`,
change the ExecStart entry to your Python path
(run `which Python` in the **Quick Start** section)
2. Copy this script under `/etc/systemd/system`
3. Reload services
```
sudo systemctl daemon-reload
```
4. Enable service at system start-up
```
sudo systemctl enable nvidia-gpu-fan-control
```
5. Start the service right now
```
sudo systemctl start nvidia-gpu-fan-control
```

## Define Profile
The default profile can be found at `profiles/default.yml`. Define your own profile is straightforward and load with --profile.
<img src="https://github.com/ypei92/fan_control_nvidia-ml-py/assets/16912644/8907d5c3-9b1c-44d7-9df4-58c421e85e47" width="500">
