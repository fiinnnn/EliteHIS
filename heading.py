# -*- coding: utf-8 -*-

import sys
import math

def calc_heading(currentLat, currentLong, targetLat, targetLong):
    """
    Calculates target heading from coordinates
    
    Args:
        currentLat: Current latitude of the player
        currentLong: Current longitude of the player
        targetLat: Target latitude
        targetLong: Target longitude

    Returns:
        Target heading in degrees
    """
    currentLat = math.radians(currentLat)
    currentLong = math.radians(currentLong)
    targetLat = math.radians(targetLat)
    targetLong = math.radians(targetLong)

    dLat = math.log(math.tan(math.pi/4 + targetLat/2) / math.tan(math.pi/4 + currentLat/2))
    dLong = targetLong - currentLong
    
    heading = math.degrees(math.atan2(dLong, dLat))
    
    if heading < 0:
        heading = heading + 360

    return int(heading)

def main():
    """
    Used to test heading calculation
    Won't be executed when loaded as a module
    """
    lat1 = float(input("lat1: "))
    lat2 = float(input("lat2: "))
    lat3 = float(input("lat3: "))
    lat4 = float(input("lat4: "))

    print(calc_heading(lat1, lat2, lat3, lat4))

if __name__ == "__main__":
    main()
