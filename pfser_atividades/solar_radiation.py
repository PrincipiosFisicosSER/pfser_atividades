import datetime
import numpy as np

from typing import Tuple


def get_julian_day(date: str, fmt="%Y-%m-%d"):
    dt = datetime.datetime.strptime(date, fmt)
    return dt.timetuple().tm_yday


def compute_day_angle(date):
    julian_day = get_julian_day(date)
    return (2 * np.pi) * ((julian_day - 1) / 365)


def compute_excentric_corr_factor(day_angle):
    ecf= ((1.000110 + 0.034221 * np.cos(day_angle) + 0.001280 * 
           np.sin(day_angle)) + 0.000719 * np.cos(2 * (day_angle))
           + 0.000077 * np.sin(2 * (day_angle)))
    return ecf

def compute_sum_declination(day_angle, degree=False):
    sum_declination = (0.006918 - 0.399912 *  np.cos(day_angle) + 
                0.070257 * np.sin(day_angle) - 0.006758 * 
                np.cos(2 * day_angle) + 0.000907 * np.sin(2 * day_angle) - 
                0.002697 * np.cos(3 * day_angle) +  0.00148 * 
                np.sin(3 * day_angle))
    
    if degree:
        sum_declination *= 180 / np.pi
    
    return sum_declination


def compute_sum_hour(time, degrees=False):

    tm = datetime.datetime.strptime(time, "%H:%M")
    x = abs(tm.hour + (tm.minute / 60) - 12)

    sum_hour = (np.pi / 12) * x
    if degrees:
        sum_hour *= 180 / np.pi
    return sum_hour


def compute_zenith_angle(sum_declination: float, 
                         sum_hour: float, lat: float) -> Tuple[float, float]:
    """Computes zenith angle in degrees and its cosine
    """
    zenith_cosine = ((np.sin(sum_declination) * np.sin(lat * np.pi / 180))
                      + (np.cos(sum_declination) * np.cos(lat * np.pi / 180)
                         * np.cos(sum_hour)))
    zenith = np.arccos(zenith_cosine) * 180 / np.pi
    
    return zenith, zenith_cosine


def compute_irradiation(correction_factor, sum_declination, sum_hour, 
                       latitude, sum_constant=1367):
    
    irradiation = (sum_constant * 3.6 * correction_factor * 
    (np.sin(sum_declination) * np.sin(latitude * np.pi / 180)
    + np.cos(sum_declination) * np.cos(latitude * np.pi / 180) * np.cos(sum_hour)))
    
    return irradiation


def compute_irradiance(irradiation):
    return irradiation / 3.6
