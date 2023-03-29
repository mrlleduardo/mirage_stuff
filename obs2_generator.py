from mirage.ramp_generator.obs_generator import Observation
from mirage.imaging_simulator import ImgSim
from mirage.dark.dark_prep import DarkPrep
from mirage.utils.read_fits import Read_fits

from glob import glob
import numpy as np

from mirage import imaging_simulator
from mirage.apt import apt_inputs
from mirage.yaml import yaml_generator

from mirage.seed_image import catalog_seed_image

from astropy.io import fits

import os
os.environ["MIRAGE_DATA"] = "/arc/projects/jwst-crds/mirage_data"
os.environ["CRDS_PATH"] = "/arc/projects/jwst-crds/crds_cache"


files = 'yaml_files/jw01568002013_01101_00026_nrcb5.yaml'  # ,'yaml_files/jw01568001018_01101_00036_nrca5.yaml']
         # 'yaml_files/jw01568002018_01101_00035_nrca5.yaml','yaml_files/jw01568002018_01101_00036_nrca5.yaml',
         # 'yaml_files/jw01568003018_01101_00035_nrca5.yaml','yaml_files/jw01568003018_01101_00036_nrca5.yaml']
        
dark_sim = 'sim_data/jw01568002013_01101_00026_nrcb5_uncal_linear_dark_prep_object.fits' 
img_sim = 'sim_data/jw01568002013_01101_00026_nrcb5_uncal_F322W2_CLEAR_final_seed_image.fits'
        

ob = Observation()
ob.paramfile = files
ob.read_parameter_file()
# ob.check_params()

dark = ob.read_dark_file(dark_sim)
dark.data *= 0.
dark.sbAndRefpix *= 0.
dark.zeroframe *= 0.
dark.zero_sbAndRefpix *= 0.

seed = ob.read_seed(img_sim)

# syn = ob.add_synthetic_to_dark(seed, dark, syn_zeroframe=None)

ob.create()