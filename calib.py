import glob
from jwst.pipeline.calwebb_detector1 import Detector1Pipeline
import os

os.environ["MIRAGE_DATA"] = "/arc/projects/jwst-crds/mirage_data"
os.environ["CRDS_PATH"] = "/arc/projects/jwst-crds/crds_cache"
os.environ['CRDS_SERVER_URL'] = 'https://jwst-crds.stsci.edu'

files = glob.glob('sim_data/*seed_image.fits')

for file in files:
    d = Detector1Pipeline.call(file, save_results=True, output_dir='/arc/projects/classy/MarsSandbox/mirage0/mirage_input_files/calib_files')
