"""
General shared configuration constants for Brokkr.
"""

# Standard library imports
import os
from pathlib import Path


# --- General global constants ---

# Package name
PACKAGE_NAME = "brokkr"

# Duration of sleep/wait tickets
SLEEP_TICK_S = 0.5


# --- Path constants ---

# Subpaths of output dir
OUTPUT_SUBPATH_LOG = Path("log")
OUTPUT_SUBPATH_MONITOR = Path("telemetry")

# Mode preset subpaths
OUTPUT_SUBPATH_DEFAULT = Path("data")
OUTPUT_SUBPATH_REALTIME = Path("realtime")
OUTPUT_SUBPATH_TEST = Path("test")

# Path for general Brokkr output
OUTPUT_PATH_BASE = Path("~", PACKAGE_NAME)
OUTPUT_PATH_DEFAULT = OUTPUT_PATH_BASE / OUTPUT_SUBPATH_DEFAULT

# Subpaths of system dir
SYSTEM_SUBPATH_CONFIG = Path("config")


# --- Config constants ---

# Config type names
CONFIG_NAME_SYSTEM = "system"
CONFIG_NAME_MODE = "mode"
CONFIG_NAME_METADATA = "metadata"
CONFIG_NAME_UNIT = "unit"
CONFIG_NAME_LOG = "log"
CONFIG_NAME_MAIN = "main"

# Config level names
LEVEL_NAME_SYSTEM = "system"
LEVEL_NAME_SYSTEM_CLIENT = "client"
LEVEL_NAME_REMOTE = "remote"
LEVEL_NAME_LOCAL = "local"

# Config variables
CONFIG_PATH_XDG = Path(
    f"~{os.environ.get('SUDO_USER', '')}/.config").expanduser()
CONFIG_PATH_LOCAL = CONFIG_PATH_XDG / PACKAGE_NAME
CONFIG_VERSION = 1
