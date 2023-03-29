#! /usr/bin/env python
"""Starting with a Horizons ephemeris file, modify and create an ephemeris for a fake target
"""
from astropy.coordinates import SkyCoord
import astropy.units as u
from copy import deepcopy
from datetime import datetime, timedelta
import numpy as np

from mirage.seed_image.ephemeris_tools import read_ephemeris_file

gk_file = 'GK56_ephemeris.txt'

offset_ras = [0., 0., 0., 0., 0.] ###idk 
offset_decs = [-1.25/3600, 0., 1.25 / 3600, 2.5 / 3600, 3.75/3600] ###idk
vel_mults = [0., 1., 1.5, 2., 3.] ##speed?

with open(gk_file) as fobj:
    lines = fobj.readlines()
header = lines[0:72]

e = read_ephemeris_file(gk_file)

base_idx = np.where(e['Time'] == datetime(2023, 1, 24, 7, 0, 0))[0][0] ### this one finds the 7am time. why 7am???
base_time = e['Time'][base_idx]
base_ra, base_dec = e['RA'][base_idx], e['Dec'][base_idx]
next_ra, next_dec = e['RA'][base_idx+20], e['Dec'][base_idx+20] ###jumps 10 hours. why???
next_time = e['Time'][base_idx+20]

base_time

e['Time'][base_idx+20]

delta_ra = next_ra - base_ra
delta_dec = next_dec - base_dec
delta_time = next_time - base_time
delta_ra_per_time = delta_ra / delta_time.seconds
delta_dec_per_time = delta_dec / delta_time.seconds

for offset_ra, offset_dec, vel_mult in zip(offset_ras, offset_decs, vel_mults):
    new_e = deepcopy(e)
    # Write the header
    offra = f'{offset_ra*3600:.2f}'
    offdec = f'{offset_dec*3600:.2f}'
    outfile = f'gk56_offset_{offra}_{offdec}_speed_up_factor_{vel_mult}_ephemeris.txt'
    with open(outfile, 'w') as fobj:
        for l in lines[0:72]:
            fobj.write(l)

        for i, row in enumerate(new_e):
            dt = row['Time'] - base_time
            new_ra = (base_ra + offset_ra) + (delta_ra_per_time * vel_mult * dt.total_seconds())  
            new_dec = (base_dec + offset_dec) + (delta_dec_per_time * vel_mult * dt.total_seconds())
            if i == base_idx:
                print(dt.seconds)
                print(base_ra, base_dec)
                print(base_dec, offset_dec, delta_dec_per_time, vel_mult, dt.total_seconds())
                print(base_ra, offset_ra, delta_ra_per_time, vel_mult, dt.total_seconds())
                print(new_ra, new_dec)
                print(base_dec + offset_dec)
            m = SkyCoord(new_ra, new_dec, unit=u.deg)
            new_ra_str, new_dec_str = m.to_string('hmsdms').split(' ')
            new_ra_str = new_ra_str.replace('h', ' ')
            new_ra_str = new_ra_str.replace('m', ' ')
            new_ra_str = new_ra_str.replace('s', ' ')
            new_dec_str = new_dec_str.replace('d', ' ')
            new_dec_str = new_dec_str.replace('m', ' ')
            new_dec_str = new_dec_str.replace('s', ' ')
            rowtime = row["Time"].strftime("%Y-%b-%d %H:%M")
            rowstr = f'{rowtime} {new_ra_str} {new_dec_str} \n'
            fobj.write(rowstr)



