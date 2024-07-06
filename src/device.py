import bisect
import logging
import pynvml as nvml
from operator import itemgetter
from typing import List, Tuple

from utils.logging import get_logger

TEMP_MIN_VALUE = 20.0 # fan is around 30%
TEMP_MAX_VALUE = 60.0 # fan is at 100% onwards
TEMP_RANGE = TEMP_MAX_VALUE - TEMP_MIN_VALUE

def fanspeed_from_t(t):
  if t <= TEMP_MIN_VALUE: return 0.0
  if t >= TEMP_MAX_VALUE: return 1.0
  return (t - TEMP_MIN_VALUE) / TEMP_RANGE

class Device:
  """Device class for one GPU."""
  def __init__(self, index: int, speed_profile: dict, log_level: int) -> None:
    self.index = index
    self.handle = nvml.nvmlDeviceGetHandleByIndex(index)
    self.name = nvml.nvmlDeviceGetName(self.handle)
    self.fan_count = nvml.nvmlDeviceGetNumFans(self.handle)
    self.fan_min, self.fan_max = self.get_device_min_max_fan_speed(self.handle)
    self.logger = get_logger(self.__class__.__name__, log_level)
    self.speed_profile = list(speed_profile.items())
    sorted(self.speed_profile, key=itemgetter(0))  # sort by temp set points

    self.logger.info(self.get_device_info_str())
    self.logger.debug(f"Fan speed set points: {self.speed_profile}")


  def get_device_info_str(self) -> str:
    return "[Device %d] %s\tfan_groups: %d\tfan_speed: %d-%d" % (self.index,
        self.name, self.fan_count, self.fan_min, self.fan_max)

  def get_device_min_max_fan_speed(self, handle) -> [int, int]:
    """Fetch fan speed limit of a certain GPU, usually 0-100."""
    c_minSpeed = nvml.c_uint()
    c_maxSpeed = nvml.c_uint()
    fn = nvml._nvmlGetFunctionPointer("nvmlDeviceGetMinMaxFanSpeed")
    ret = fn(handle, nvml.byref(c_minSpeed), nvml.byref(c_maxSpeed))
    nvml._nvmlCheckReturn(ret)
    return c_minSpeed.value, c_maxSpeed.value

  def reset_to_default_policy(self) -> None:
    """Reset fan policy to default."""
    for i in range(self.fan_count):
      nvml.nvmlDeviceSetDefaultFanSpeed_v2(self.handle, i)

  def get_cur_temp(self) -> int:
    return nvml.nvmlDeviceGetTemperature(self.handle, nvml.NVML_TEMPERATURE_GPU)

  def get_cur_fan_speed(self) -> int:
    speeds = [nvml.nvmlDeviceGetFanSpeed_v2(self.handle, i) for i in range(self.fan_count)]
    return int(sum(speeds)/len(speeds))

  def set_fan_speed(self, percentage) -> None:
    """
    Manually set the new fan speed.
    WARNING: This function changes the fan control policy to manual.
    It means that YOU have to monitor the temperature and adjust the fan speed accordingly.
    If you set the fan speed too low you can burn your GPU!
    Use nvmlDeviceSetDefaultFanSpeed_v2 to restore default control policy.
    """
    for i in range(self.fan_count):
      nvml.nvmlDeviceSetFanSpeed_v2(self.handle, i, percentage)

  def calc_fan_speed(self, t: int, speed_profile: List[Tuple[int, int]]) -> int:
    """Calcute the desired speed given a temperature."""
    idx = bisect.bisect_right(speed_profile, t, key=itemgetter(0))
    new_speed = speed_profile[-1][1]  # max speed
    match idx:
      case 0:  # min speed
        new_speed = speed_profile[0][1]
      case 4:  # max speed
        new_speed = speed_profile[-1][1]
      case _:
        l_t = speed_profile[idx - 1][0]
        r_t = speed_profile[idx][0]
        l_s = speed_profile[idx - 1][1]
        r_s = speed_profile[idx][1]
        assert (l_t != r_t)
        slope = (r_s - l_s) / (r_t - l_t)
        new_speed = l_s + slope * (t - l_t)

    return int(new_speed)

  def control(self) -> None:
    """Calculate new speed and compare with old speed, set new speed if different"""
    t = self.get_cur_temp()
    new_speed = self.calc_fan_speed(t, self.speed_profile)
    cur_speed = self.get_cur_fan_speed()

    if(new_speed != cur_speed):
      self.logger.info(f"{self.index}:{self.name}\ttemp:{t}\tspeed: {cur_speed}>>{new_speed}")
      self.set_fan_speed(new_speed)
