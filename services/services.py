from random import randint

def get_point_location() -> float:
    location_latitude = randint(-30, 60) + randint(20000, 70000) * 0.00001
    return location_latitude