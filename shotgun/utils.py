import datetime as DT
import os
from base64 import b64decode
import re
from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def is_past_date(date_string):
    date = DT.datetime.strptime(date_string, '%a, %d %b %Y').date()
    return date < DT.datetime.now().date()


def is_valid_geolocation(lat, lng):
    # Validates geographic coordinates.
    try:
        return len(lat) <= 16 and len(lng) <= 16 and 90 > float(lat) > -90 and 180 > float(lng) > -180
    except ValueError:
        return False


def is_valid_rating(stars):
    try:
        return 1 <= int(stars) <= 5
    except ValueError:
        return


def is_valid_username(username):
    # Validates a username.
    return re.match(r'^[A-Za-z0-9_-]+$', username) and 3 <= len(username) <= 16


def is_valid_password(password):
    # Validates a password.
    return password.isprintable() and len(password) >= 6


def save_image(data, filename):
    # Saves a base64-encoded image.
    with open(filename, 'wb') as f:
        f.write(b64decode(data.encode('ascii')))


def check_image_ext(filename):
    # Checks whether the image file format is allowed.
    _, ext = os.path.splitext(filename)
    return ext in ['.jpg']
