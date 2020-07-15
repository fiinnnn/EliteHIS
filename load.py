import sys

import tkinter as tk

import myNotebook as nb
from config import config

import utils
import overlay

this = sys.modules[__name__]

def plugin_start3(plugin_dir):
	return plugin_start()

def plugin_start():
    """
    Load EliteHIS plugin
    """
    #Initialize target coordinates and planet radius
    this.targetLat = tk.DoubleVar(value=0)
    this.targetLong = tk.DoubleVar(value=0)
    this.planetRadius = tk.IntVar(value=0)

    print("EliteHIS: loaded")
    return "EliteHIS"

def plugin_stop():
    """
    Stop EliteHIS plugin
    """
    print("EliteHIS: stopped")

def plugin_prefs(parent, cmdr, is_beta):
    """
    Create settings dialog
    """
    frame = nb.Frame(parent)

    nb.Label(frame, text="Latitude").grid(row=0)
    nb.Entry(frame, textvariable=this.targetLat).grid(row=0, column=1)

    nb.Label(frame, text="Longitude").grid(row=1)
    nb.Entry(frame, textvariable=this.targetLong).grid(row=1, column=1)

    nb.Label(frame, text="Planet radius (in metres)").grid(row=2)
    nb.Entry(frame, textvariable=this.planetRadius).grid(row=2, column=1)
    return frame

def dashboard_entry(cmdr, is_beta, entry):
    """
    Called when something on the cockpit display changes
    """
    #Lat/Long not always in status.json
    try:
        currentLat = entry["Latitude"]
        currentLong = entry["Longitude"]
        altitude = entry["Altitude"]
        recalculate_info(currentLat, currentLong, altitude)
    except KeyError:
        pass

def recalculate_info(currentLat, currentLong, altitude):
    """
    Recalculate target heading
    """
    heading = utils.calc_heading(currentLat, currentLong, this.targetLat.get(), this.targetLong.get())
    overlay.show_heading(heading)
    
    if this.planetRadius.get() > 0:
        distance = utils.calc_distance(currentLat, currentLong, this.targetLat.get(), this.targetLong.get(), this.planetRadius.get(), altitude)
        overlay.show_distance(distance)
