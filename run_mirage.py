import os
os.environ["MIRAGE_DATA"] = "/arc/projects/jwst-crds/mirage_data"
os.environ["CRDS_PATH"] = "/arc/projects/jwst-crds/crds_cache"
os.environ["PYTHONPATH"] = "/arc/home/meduardo/git/mirage/mirage:$PYTHONPATH"


# import mirage
# help(mirage)

from mirage.imaging_simulator import ImgSim
from glob import glob

from mirage import imaging_simulator
from mirage.apt import apt_inputs
from mirage.yaml import yaml_generator

from mirage.seed_image import catalog_seed_image



# files = sorted(glob('yaml_files/jw01568001001_01101_00001_nrca*.yaml'))

# files = ['yaml_files/jw01568001013_01101_00025_nrcb2.yaml', 'yaml_files/jw01568001013_01101_00026_nrcb2.yaml',
#          'yaml_files/jw01568001013_01101_00025_nrcb5.yaml', 'yaml_files/jw01568001013_01101_00026_nrcb5.yaml',
#          'yaml_files/jw01568002013_01101_00025_nrcb2.yaml', 'yaml_files/jw01568002013_01101_00026_nrcb2.yaml',
#          'yaml_files/jw01568002013_01101_00025_nrcb5.yaml', 'yaml_files/jw01568002013_01101_00026_nrcb5.yaml']

files = ['yaml_files/jw01568002013_01101_00025_nrcb5.yaml', 'yaml_files/jw01568002013_01101_00026_nrcb5.yaml']

# for yaml_file in files:
#     sim = ImgSim(paramfile=yaml_file)
#     sim.create()
    

for yaml_file in files:
    cat = catalog_seed_image.Catalog_seed()
    cat.paramfile=yaml_file
    cat.make_seed()
    
