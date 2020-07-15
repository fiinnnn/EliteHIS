import sys
import math

from collections import namedtuple

Point = namedtuple("Point", ["x", "y", "z"])

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

    return int(round(heading))

def calc_distance(currentLat, currentLong, targetLat, targetLong, planetRadius, altitude):
    """
    Calculates the distance to the target

    Args:
        currentLat: Current latitude of the player
        currentLong: Current longitude of the player
        targetLat: Target latitude
        targetLong: Target longitude
        planetRadius: Radius of the current planet in m
        altitude: Altitude of the player in m

    Returns:
        Target distance in m
    """
    currentLat = math.radians(currentLat)
    currentLong = math.radians(currentLong)
    targetLat = math.radians(targetLat)
    targetLong = math.radians(targetLong)

    player = polar_to_euclidean(currentLat, currentLong, planetRadius + altitude)
    target = polar_to_euclidean(targetLat, targetLong, planetRadius)

    distance = math.sqrt(math.pow(target.x - player.x, 2) + math.pow(target.y - player.y, 2) + math.pow(target.z - player.z, 2))
    return distance

def polar_to_euclidean(lat, lon, r):
    """
    Converts from polar coordinates to euclidean coordinates

    Args:
        lat: Latitude in radians
        lon: Longitude in radians
        r: Planet radius + altitude

    Returns:
        Euclidean coordinates
    """
    x = r * math.sin(lon) * math.cos(lat)
    y = r * math.sin(lon) * math.sin(lat)
    z = r * math.cos(lon)

    return Point(x, y, z)

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
