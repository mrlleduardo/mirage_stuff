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


def read_seed(filename):
    with fits.open(filename) as h:
        seed = h[1].data
        seedheader = h[0].header
        try:
            segmap = h[2].data
        except:
            segmap = None
    return seed, segmap, seedheader
    
    
def read_dark_file(filename):

    obj = Read_fits()
    obj.file = filename
    obj.read_astropy()
    return obj


img_sim = 'sim_data/jw01568002013_01101_00026_nrcb5_uncal_F322W2_CLEAR_final_seed_image.fits'
han = fits.open(img_sim)
data = han[1].data
header = han[1].header
han.close()

#for i in header:
#    print(i,header[i])
#exit()
# files = glob.glob('/sim_data/*seed_image.fits')

files = 'yaml_files/jw01568002013_01101_00026_nrcb5.yaml'  # ,'yaml_files/jw01568001018_01101_00036_nrca5.yaml']
         # 'yaml_files/jw01568002018_01101_00035_nrca5.yaml','yaml_files/jw01568002018_01101_00036_nrca5.yaml',
         # 'yaml_files/jw01568003018_01101_00035_nrca5.yaml','yaml_files/jw01568003018_01101_00036_nrca5.yaml']

        
dark_sim = 'sim_data/jw01568002013_01101_00026_nrcb5_uncal_linear_dark_prep_object.fits' 

dark = read_dark_file(dark_sim)
seed = read_seed(img_sim)

dark.data *= 0.
dark.sbAndRefpix *= 0.
dark.zeroframe *= 0.
dark.zero_sbAndRefpix *= 0.

# for f in files:
ob = Observation()
ob.paramfile = files
ob.read_parameter_file()
ob.readpattern_check()
# ob.check_params()

# print(list(ob.params.keys()))
# print(ob.params['Readout'])

########################################
runStep = {'cosmicray': 0}
ob.runStep = runStep
ob.params['Readout']['nframe'] = 2
ob.params['Readout']['nskip']=0
ob.gain = 1.              ##fix this?

# exit()
# print(data[0].shape)
########################################

'''
data : numpy.ndarray
            Seed image. Should be a 2d frame or 3d integration.
            If the original seed image is a 4d exposure, call frame_to_ramp
            with one integration at a time.
'''

outramp1, zeroframe1 = ob.frame_to_ramp(data[0]) ###adds with poisson noise to seed image. Outputs ramp and zeroframe.
outramp2, zeroframe2 = ob.frame_to_ramp(data[1])
outramp3, zeroframe3 = ob.frame_to_ramp(data[2])

allramp = np.stack((outramp1,outramp2,outramp3),axis=0)
frame0 = np.stack((zeroframe1,zeroframe2,zeroframe3),axis=0)
    
# outramp, zeroframe = ob.frame_to_ramp_no_cr(data[0]) ###can't pass but works with frame_to_ramp

# print(outramp1.shape, zeroframe1.shape, allramp.shape, frame0.shape)

PrimaryHDU = fits.PrimaryHDU(allramp)
HDU_list = fits.HDUList([PrimaryHDU])
HDU_list.writeto('allramp.fits', overwrite=True)


# print(zeroframe, np.min(zeroframe), np.max(zeroframe))

syn = ob.add_synthetic_to_dark(allramp, dark, syn_zeroframe=frame0)
# print(syn[0].shape, syn[1].shape, syn[2].shape)

'''
        synthetic : numpy.ndarray
            4D exposure containing combined simulated + dark data
        zeroframe : numpy.ndarray
            Zeroth read(s) of simulated + dark data
        reorder_sbandref : numpy.ndarray
            superbias and refpix signal from the dark
'''

PrimaryHDU = fits.PrimaryHDU(syn[0])
HDU_list = fits.HDUList([PrimaryHDU])
HDU_list.writeto('synthetic1.fits', overwrite=True)

PrimaryHDU = fits.PrimaryHDU(syn[1])
HDU_list = fits.HDUList([PrimaryHDU])
HDU_list.writeto('frame01.fits', overwrite=True)

PrimaryHDU = fits.PrimaryHDU(syn[1])
HDU_list = fits.HDUList([PrimaryHDU])
HDU_list.writeto('superbias_refpix1.fits', overwrite=True)

# ob.create()
