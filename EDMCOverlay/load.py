"""
Plugin for EDMCOverlay
"""
import time

from edmcoverlay import ensure_service, Overlay, shutdown_service

client = Overlay()


def plugin_start():
    """
    Start our plugin, add this dir to the search path so others can use our module
    :return:
    """
    ensure_service()
    time.sleep(2)
    try:
        client.send_message("_", "EDMC Overlay Ready", "#ffa500", 5, 5, ttl=5, size="large")
    except Exception:
        pass
    return "EDMCOverlay"


def journal_entry(cmdr, system, station, entry, state):
    """
    Make sure the service is up and running
    :param cmdr:
    :param system:
    :param station:
    :param entry:
    :param state:
    :return:
    """
    ensure_service()

def plugin_stop():
    """
    Stop this plugin and shutdown running overlay service
    :return:
    """
    shutdown_service()
