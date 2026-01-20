
def calc_antenna(freq_mhz, velocity_factor=0.95):
    
    
    
    if freq_mhz <= 0: return 0,0,0,0
    
    
    wavelength_m = 299.792 / freq_mhz
    
    
    
    
    dipole_total_m = (wavelength_m / 2) * velocity_factor
    
    
    dipole_leg_m = dipole_total_m / 2
    
    
    quarter_wave_m = (wavelength_m / 4) * velocity_factor
    
    return wavelength_m, dipole_total_m, dipole_leg_m, quarter_wave_m
