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
    this.overlay.send_message("heading", "Heading: " + str(heading), "#ff7100", 100, 100, 8)
