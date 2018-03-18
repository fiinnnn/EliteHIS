# -*- coding: utf-8 -*-

import sys

import Tkinter as tk
import myNotebook as nb
from config import config

import heading
import overlay

this = sys.modules[__name__]

def plugin_start():
    """
    Load EliteHIS plugin
    """
    #Initialize target coordinates
    this.targetLat = tk.DoubleVar(value=-29.1664)
    this.targetLong = tk.DoubleVar(value=-30.5041)

    print("EliteHIS: loaded")
    return "EliteHIS"

def plugin_stop():
    """
    Stop EliteHIS plugin
    """
    #Close EDMCOverlay
    overlay.shutdown_overlay()
    print("EliteHIS: stopped")

def plugin_prefs(parent, cmdr, is_beta):
    """
    Create settings dialog
    """
    frame = nb.Frame(parent)

    nb.Label(frame, text="Latitude").grid()
    nb.Entry(frame, textvariable=this.targetLat).grid()

    nb.Label(frame, text="Longitude").grid()
    nb.Entry(frame, textvariable=this.targetLong).grid()

    return frame

def dashboard_entry(cmdr, is_beta, entry):
    """
    Called when something on the cockpit display changes
    """
    #Lat/Long not always in status.json
    try:
        currentLat = entry['Latitude']
        currentLong = entry['Longitude']
        recalculate_heading(currentLat, currentLong)
    except KeyError:
        pass

def recalculate_heading(currentLat, currentLong):
    """
    Recalculate target heading
    """
    targetHeading = heading.calc_heading(currentLat, currentLong, this.targetLat.get(), this.targetLong.get())
    overlay.show_heading(targetHeading)
