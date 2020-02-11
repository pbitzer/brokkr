"""
Static configuration for Brokkr; loaded after primary initialization.
"""

# Standard library imports
import logging

# Local imports
import brokkr.config.handlers


logger = logging.getLogger(__name__)


# Master config dict; currently static
STATIC_CONFIG_HANDLER = brokkr.config.handlers.CONFIG_HANDLER_STATIC
logger.debug(
    "Reading static config at system path %r and local path %r",
    STATIC_CONFIG_HANDLER.config_type.main_config_path.as_posix(),
    STATIC_CONFIG_HANDLER.config_type.preset_config_path.as_posix(),
    )

CONFIGS = STATIC_CONFIG_HANDLER.read_configs()
logger.debug("Loaded static config: %r", CONFIGS)
CONFIG = STATIC_CONFIG_HANDLER.render_config(CONFIGS)
logger.info("Rendered static config: %r", CONFIG)