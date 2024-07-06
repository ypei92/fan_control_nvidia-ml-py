import logging
import pynvml as nvml
import time

from device import Device
from utils.cmd_parser import cmd_parser
from utils.speed_profile import check_speed_profile
from utils.miscs import load_yaml
from utils.logging import init_root_logger, get_logger


def main():
  # parse command line options
  args = cmd_parser()

  # get logger
  init_root_logger(args.log_level == logging.DEBUG)
  logger = get_logger("main", args.log_level)
  logger.debug(args)

  # load fan speed profile (TODO: check if profile is valid)
  speed_profile = load_yaml(args.profile)
  check_speed_profile(speed_profile)

  # initialize nvidia management lib
  nvml.nvmlInit()

  # initialize devices
  logger.info(f"Driver Version: {nvml.nvmlSystemGetDriverVersion()}")
  li_devices = []
  for i in range(nvml.nvmlDeviceGetCount()):
    device = Device(i, speed_profile, args.log_level)
    li_devices.append(device)

  # fan control service (reset to default upon exit)
  try:
    while True:
      for device in li_devices:
        device.control()
      time.sleep(args.control_interval)

  finally:
    logger.info("Reset to the default fan control policy!")
    for device in li_devices:
      device.reset_to_default_policy()

  # end nvidia management lib
  nvml.nvmlShutdown()


if __name__ == "__main__":
  main()
