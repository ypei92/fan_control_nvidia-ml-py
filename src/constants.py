import os
import pathlib


# Directory structure
REPO_NAME = "fan_control_nvidia-ml-py"
#WORK_DIR = os.path.join(pathlib.Path.home(), '.' + REPO_NAME)
WORK_DIR = os.path.join(pathlib.Path.home(), 'scripts/' + REPO_NAME)
LOG_DIR = os.path.join(WORK_DIR, "logs")
PROFILE_DIR = os.path.join(WORK_DIR, "profiles")
DEFAULT_PROFILE_FILE = os.path.join(PROFILE_DIR, "default.yml")

# Fan control related
DEFAULT_CTRL_INTERVAL_SEC = 1.0  # seconds

# Log related
LOG_FILENAME = "fan_speed.log"
LOG_SIZE_LIMIT_MB = 1  # MB
LOG_FMT_BOLD = '\033[1m'
LOG_FMT_END = '\033[0m'
