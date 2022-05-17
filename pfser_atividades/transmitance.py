import numpy as np
import functools
import operator
import collections

def optical_path(height, cos_zenith_angle):
    """Returns the lenght optical path of EMR given a height and the zenith
    angle (degrees).

    Paramenters
    -----------
    height: float or array like
        height (in some lengh unit)
    cos zenith_angle: float
        cosine of zeinith angle

    """

    return height / cos_zenith_angle


def compute_transmitance(optical_path, coefficients):
    """Returns the transmitance given optical path and attenuatation coefficient

    Notes
    -----
    optical path and attenuation coefficient must have compatible units.

    """

    transmitance = {wavelength: np.exp(-optical_path * coefficient)
                    for wavelength, coefficient in coefficients.items()}

    return transmitance


def compute_coefficients(gas_cross_sections, molecule_density):
    coefficients = {wavelength: cross_section * molecule_density 
                    for wavelength, cross_section in gas_cross_sections.items()}
    return coefficients



def aggregate_coefficients(gas_coefficients_list):
    aggregated_coefficients = dict(functools.reduce(
        operator.add, map(collections.Counter, gas_coefficients_list)))
    return aggregated_coefficients


def compute_attenuation(irradiance, transmitance):
    attenuation = {key: irradiance[key] * transmitance[key]
                   for key in irradiance.keys()}

    return attenuation


def compute_wavenumber(wavelength):
    """Compute wavenumber (1/cm) given wave lenght (nm)"""
    
    
    return 1 / (wavelength * 10 ** -7)


def correct_refraction_index_scale(refraction_index):
    return refraction_index * (10 ** -8) + 1


def compute_rayleigh_cross_section(refraction_index_function,
                                   king_correction_factor_function,
                                   wavelengths,
                                   molecule_density=2.546899 * 10 ** 19):
    
    wavelength_list = np.array([int(wavelength[:3]) for wavelength in wavelengths])
    wavenumber = compute_wavenumber(wavelength_list)
    refraction_index = correct_refraction_index_scale(
        refraction_index_function(wavenumber)
    )
    king_correction_factor = king_correction_factor_function(wavenumber)
    
    const = 24 * (np.pi ** 3)
    aux =  const * (wavenumber ** 4) / (molecule_density ** 2)
    lorentz_ratio = (refraction_index ** 2 - 1) / (refraction_index ** 2 + 2)

    
    cross_sections_list = aux * (lorentz_ratio ** 2) * king_correction_factor

    cross_sections = {wavelength: cross_section 
                      for wavelength, cross_section in zip(wavelengths,
                                                           cross_sections_list)}

    return cross_sections