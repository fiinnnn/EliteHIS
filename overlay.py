# -*- coding: utf-8 -*-

import sys

this = sys.modules[__name__]

#Load EDMCOverlay
try:
    from EDMCOverlay import edmcoverlay
except ImportError:
    print("EliteHIS: Unable to load EDMCOverlay")

this.overlay = edmcoverlay.Overlay()

def show_heading(heading):
    this.overlay.send_message("heading", "Heading: " + str(heading), "#ff7100", 2, 2, 8, "large")
    #this.overlay.send_message("distance", "Distance: ", "#ff7100", 2, 25, 8, "large")

def shutdown_overlay():
    edmcoverlay.shutdown()
