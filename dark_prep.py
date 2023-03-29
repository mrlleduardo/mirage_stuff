from mirage.dark.dark_prep import DarkPrep
import mirage
import os

os.environ["MIRAGE_DATA"] = "/arc/projects/jwst-crds/mirage_data"
os.environ["CRDS_PATH"] = "/arc/projects/jwst-crds/crds_cache"


dark = DarkPrep()
dark.paramfile = 'yaml_files/jw01568002013_01101_00026_nrcb5.yaml'
dark.prepare()
