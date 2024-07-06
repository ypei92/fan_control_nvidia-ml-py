import os
import yaml
import traceback
import logging


def raise_exception(msg: str, print_stack: bool = True) -> None:
  """Helper method to raise exception with msg and logging."""
  # stack is a keyword-only argument
  if print_stack:
      traceback.print_stack()

  logger = logging.getLogger()  # root logger
  logger.error(msg=msg)

  raise Exception(msg)


def create_dir(path: str) -> None:
  """Create a folder depend on whether it exists."""
  if not os.path.exists(path):
      os.makedirs(path, exist_ok=True)


def load_yaml(path, loader=yaml.FullLoader) -> dict:
  """Utility function to load yaml file."""
  with open(path) as f:
    return yaml.load(f, Loader=loader)
