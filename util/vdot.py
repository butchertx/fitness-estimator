"""
Based on the vdot_calculator Module (https://pypi.org/project/vdot-calculator/)

This module provides functions for calculating VDOT (Volume of Oxygen)
values based on the original Jack Danniels Running Formula.
bibliography:
https://www.letsrun.com/forum/flat_read.php?thread=3704747
https://www.letsrun.com/forum/flat_read.php?thread=4858970

"""

import math


def daniels_vdot(time_minutes: float, total_distance: float) -> float:
    """
     Calculate the VO2max using the Daniels Method.

     Parameters:
     - time_minutes (float): The total running time in minutes.
     - total_distance (float): The total running distance in meters.

     Returns:
     - float: The calculated VO2max.
     """
    velocity = total_distance / time_minutes
    percent_max = 0.8 + 0.1894393 * math.e ** (-0.012778 * time_minutes) + \
        0.2989558 * math.e ** (-0.1932605 * time_minutes)
    vo2 = -4.60 + 0.182258 * velocity + 0.000104 * velocity ** 2
    vo2max = vo2 / percent_max
    return vo2max


if __name__ == "__main__":
    # Usage example
    
    time_minutes = 5 + 41./60
    total_distance = 1609.34  # meters in a mile
    print(daniels_vdot(time_minutes, total_distance)) # should give 51.4