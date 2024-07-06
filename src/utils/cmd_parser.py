import argparse
import logging

import constants as Const

def cmd_parser() -> dict:
  """Commandline parser."""
  parser = argparse.ArgumentParser(prog="Nvidia GPU Fan Control with nvidia-ml-py")

  parser.add_argument('-p', '--profile',
                      type=str,
                      default=Const.DEFAULT_PROFILE_FILE,
                      help="Fan speed profile file.")
  parser.add_argument('-l', '--log-level',
                      default=logging.INFO,
                      type=lambda level: getattr(logging, level),
                      help="Configure the logging level.")
  parser.add_argument('-i', '--control-interval',
                      type=float,
                      default=Const.DEFAULT_CTRL_INTERVAL_SEC,
                      help="Fan control interval in seconds.")

  args = parser.parse_args()
  return args
