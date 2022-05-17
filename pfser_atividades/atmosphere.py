import numpy as np


__standard_atmospheric_gas_composition = {
    'nitrogen': 7.8084e-1,
    'oxigen': 2.0948e-1,
    'argon': 9.34e-3,
    'carbon_dioxide':3.6e-4,
    'methane':1.7e-6,
    # 'nitrogen_dioxide': 
}


def estimate_atm_temperature_EAM(height):
    """Estimates atmospheric temperature (Kelvin) given height (meters) above
    surface, using Earth Atmospheric Model.

    Parameters
    ----------
    height: numpy array
        height above surface in meters

    Notes
    -----
    For more information see:
    https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html

    """
    
    t = np.zeros(shape=height.shape)

    # masks for each atmosferic layer
    mask_1 = height <= 11000
    mask_2 = (height > 11000) & (height <= 25000)
    mask_3 = height > 25000

    t[mask_1] = 15.04 - 0.00649 * height[mask_1]
    t[mask_2] = -56.46
    t[mask_3] = -131.21 + .00299 * height[mask_3]


    return t + 273.1


def estimate_atm_pressure(height):
    """Estimates atmospheric pressure (Pa) given height above
    surface , using formula provided by Lund (through M. Iqbaun)

    Parameters
    ----------
    height: numpy array
        height above surface in meters
    
    Notes
    -----
    For more information on this method please see M. Iqbaum cap.5
    (section 5.7 p.99)
    """

    pressure = 10 ** 5 * np.exp(- 0.0001184 * height)

    return pressure


def estimate_atm_pressure_EAM(height, temperature):
    """Estimates atmospheric pressure (Pa) given height above
    surface and temperature, , using Earth Atmospheric Model.

    Parameters
    ----------
    height: numpy array
        height above surface in meters
    temperature: numpy array
        temperature in  Kelvin

    Notes
    -----
    For more information see:
    https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html

    """
    
    p = np.zeros(shape=height.shape)

    # masks for each atmosferic layer
    mask_1 = height <= 11000
    mask_2 = (height > 11000) & (height <= 25000)
    mask_3 = height > 25000

    p[mask_1] = 101.29 * np.power(temperature[mask_1] / 288.6, 5.256)
    p[mask_2] = 22.65 * np.exp(1.73 - 0.000157 * height[mask_2])
    p[mask_3] = 2.488 * np.power(temperature[mask_3] / 216.6, -11.388)

    return p * 1000


def get_atm_molecular_density(temperature, pressure):
    """Computes molecuar density (mol per cm³) given temperature (Celsius
    degrees) and pressure (kPa)

    Parameters
    ----------
    temperature, pressure: numpy array size n
        temperature in Kelvin and pressure in Pa

    """

    r = 8.314 # gas constant
    v = 0.000001 # volume of a cubic centimeter in m³
    a = 6.022 * (10 ** 23) # Avogrado constant

    return a * (v / r) * np.divide (pressure, temperature)


def compute_gases_density(
    air_molecule_density,
    atmosphere_composition=__standard_atmospheric_gas_composition
    ):

    gases_density = {wavelength: air_molecule_density * gas_fraction 
                     for wavelength, gas_fraction in atmosphere_composition.items()}
    return gases_density
