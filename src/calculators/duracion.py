def calculate_flight_duration(distance_km):
    cruise_speed = 800.0
    cruise_time_hours = distance_km / cruise_speed
    cruise_time_min = cruise_time_hours * 60
    extra_time_min = 30
    total_duration = cruise_time_min + extra_time_min

    return int(round(total_duration))


def minutes_to_hours_format(minutes):
    hours = minutes // 60
    mins = minutes % 60

    if hours > 0 and mins > 0:
        return f"{hours}h {mins}min"
    elif hours > 0:
        return f"{hours}h"
    else:
        return f"{mins}min"