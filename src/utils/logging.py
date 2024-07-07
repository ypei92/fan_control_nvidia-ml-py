import os
import logging
import logging.handlers

import constants as Const
from utils.miscs import create_dir


def init_root_logger(is_debug_mode: bool = False) -> None:
  """Initialize the root logger to files."""
  # Get root logger
  logger = logging.getLogger()

  # Create file rotating handler
  create_dir(Const.LOG_DIR)
  file_log_path = os.path.join(Const.LOG_DIR, Const.LOG_FILENAME)
  file_log_fmt = "%(asctime)s | %(filename)s:%(funcName)s | %(levelname)s: %(message)s"

  file_handler = logging.handlers.RotatingFileHandler(
      filename=file_log_path,
      mode='a',
      maxBytes=Const.LOG_SIZE_LIMIT_MB * 1024 * 1024,
      backupCount=2,
      encoding=None,
      delay=0)
  file_handler.setFormatter(logging.Formatter(file_log_fmt))
  logger.addHandler(file_handler)

  # Create streaming handler if log_level is DEBUG
  if is_debug_mode:
    console_log_fmt = (Const.LOG_FMT_BOLD
                       + "%(filename)s:%(funcName)s | [%(levelname)s] "
                       + Const.LOG_FMT_END + "%(message)s")

    # Define a console logger
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(console_log_fmt))
    logger.addHandler(console_handler)


def get_logger(name: str, log_level: int) -> logging.Logger:
  """Get a logger using a specific name and set verbosity level before return."""
  logger = logging.getLogger(name)
  logger.setLevel(log_level)

  return logger
