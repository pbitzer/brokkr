"""
High-level functions to monitor and record sensor and sunsaver status data.
"""

# Standard library imports
import collections
import datetime
import logging
import os
from pathlib import Path
import threading

# Local imports
from config.main import CONFIG
import output
import sensor
import sunsaver
import utils


_TRUTHY = "This is truthy"
_FALSY = "This is falsy"
StatusDataItem = collections.namedtuple(
    'StatusDataItem', ("name", "fn", "unpack"))
STATUS_DATA_ITEMS = (
    StatusDataItem("time", datetime.datetime.utcnow, False),
    StatusDataItem("runtime", utils.start_time_offset, False),
    StatusDataItem("ping", sensor.ping, False),
    StatusDataItem("sunsaver", sunsaver.get_sunsaver_data, True),
    StatusDataItem("hs", sensor.get_hs_data, True),
    )

logger = logging.getLogger(__name__)


def get_status_data(status_data_items=STATUS_DATA_ITEMS):
    status_data = {}
    for item in status_data_items:
        output_data = item.fn()
        if item.unpack:
            status_data.update(output_data)
        else:
            status_data[item.name] = output_data
    return status_data


def record_status_data(output_path=CONFIG["monitor"]["output_path"],
                       verbose=False):
    status_data = get_status_data()
    logger.debug("Status data: %s", status_data)
    if verbose:
        print("Status data: {status_data}".format(status_data=status_data))
    if not output_path.suffix:
        output_path = output.determine_output_filename(output_path)
    logger.debug("Writing monitoring output to file: %s",
                 str(output_path).replace(os.sep, "/"))
    output.write_line_csv(status_data, output_path)
    return status_data


def start_monitoring(
        output_path=CONFIG["monitor"]["output_path"],
        monitor_interval=CONFIG["monitor"]["interval_log_s"],
        sleep_interval=CONFIG["monitor"]["interval_sleep_s"],
        verbose=False,
        exit_event=threading.Event(),
        ):
    if not Path(output_path).suffix:
        logger.debug("Ensuring monitoring directory at: %s", output_path)
        os.makedirs(output_path, exist_ok=True)

    while not exit_event.is_set():
        try:
            record_status_data(output_path, verbose=verbose)
        except Exception as e:  # Keep logging if an error occurs
            logger.critical("%s caught at main level: %s",
                            type(e).__name__, e)
            logger.info("Details:", exc_info=1)
        next_time = (utils.monotonic_ns() + monitor_interval * 1e9
                     - (utils.monotonic_ns() - utils.START_TIME)
                     % (monitor_interval * 1e9))
        while not exit_event.is_set() and utils.monotonic_ns() < next_time:
            exit_event.wait(min([sleep_interval,
                                 (next_time - utils.monotonic_ns()) / 1e9]))
    exit_event.clear()