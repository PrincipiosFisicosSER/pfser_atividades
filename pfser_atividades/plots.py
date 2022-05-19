from cmath import phase
from matplotlib import pyplot as plt
import numpy as np

from pfser_atividades import transmitance


__style = {
    '460nm': {
        'color': 'blue',
        'line': 'solid'
    },
    '540nm': {
        'color': 'green',
        'line': 'solid'
    },
    '650nm': {
        'color': 'red',
        'line': 'solid'
    },
    '760nm': {
        'color': 'red',
        'line': 'dashed'
    },
    '800nm': {
        'color': 'red',
        'line': 'dashdot'
    },
}


def plot_transmitance(transmitance, attenuation, altitude,
                      style=__style, water=False):
    
    if water:
        corrected_altitude = altitude
        altitude_label = 'depth (m)'
    else:
        corrected_altitude  = altitude[::-1] / 100
        altitude_label = 'altitude (m)'
    
    _, ax = plt.subplots(1, ncols=2, figsize=(15, 7))

    for key, config in style.items():
        ax[0].plot(transmitance[key], corrected_altitude, color=config['color'], 
                   linestyle=config['line'], label=key)
        ax[1].plot(attenuation[key], corrected_altitude, color=config['color'],
                   linestyle=config['line'], label=key)
    

    ax[0].set_xlabel('transmitance')
    ax[1].set_xlabel(u'irradiance (W/m\u00b2.nm)')

    ax[0].set_ylabel(altitude_label)
    ax[1].set_ylabel(altitude_label)

    ax[0].legend()
    ax[1].legend()

    ax[0].xaxis.set_ticks_position('top')
    ax[0].xaxis.set_label_position('top')

    ax[1].xaxis.set_ticks_position('top')
    ax[1].xaxis.set_label_position('top')

    if water:
        ax[0].invert_yaxis()
        ax[1].invert_yaxis()

    return ax


def plot_rayleigh_phase_function(style=__style, constant=1e12, points=100):

    _, ax = plt.subplots(subplot_kw={'projection': 'polar'},
                           figsize=(20, 10))
    
    scattering_angle = np.linspace(0, 2*np.pi, num=50, endpoint=True)
    phase_function = constant * transmitance.compute_rayleigh_phase_function(
        scattering_angle)

    for key, config in style.items():
        wavelength_phase_function = phase_function / int(key[:3]) ** 4
        ax.plot(scattering_angle, wavelength_phase_function,
                color=config['color'], label=key)

    ax.legend()

    return ax
