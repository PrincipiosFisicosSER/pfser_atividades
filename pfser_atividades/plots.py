from matplotlib import pyplot as plt


def plot_transmitance(transmitance, attenuation, altitude, style, water=False):

    altitude = altitude[::-1]
    
    if water:
        corrected_altitude = altitude
        altitude_label = 'depth (m)'
    else:
        corrected_altitude  = altitude / 100
        altitude_label = 'altitude (m)'
    
    fig, ax = plt.subplots(1, ncols=2, figsize=(15, 7))

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

    return ax
