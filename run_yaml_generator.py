from mirage.yaml import yaml_generator
from glob import glob
import os

os.environ["MIRAGE_DATA"] = "/arc/projects/jwst-crds/mirage_data"

xml_file = '/arc/projects/classy/MarsSandbox/mirage0/mirage_input_files/JW_GK56.xml'
pointing_file = xml_file.replace('.xml', '.pointing')

# Run the yaml_generator
ptsrc_catalog = '/arc/projects/classy/MarsSandbox/mirage0/mirage_input_files/catalogs/catalog_1800.0.cat'
galaxy_catalog = '/arc/projects/classy/MarsSandbox/mirage0/mirage_input_files/catalogs/galaxies.cat'
mt_cat = '/arc/projects/classy/MarsSandbox/mirage0/mirage_input_files/catalogs/tnos.cat'

cat_dict = {'ECLIPTIC-RA12H': {'point_source': ptsrc_catalog,
                               'galaxy': galaxy_catalog,
                               'moving_pointsource': 'none'},
            'ECLIPTIC-RA0H': {'point_source': 'none'}
            }
# cat_dict = {'ECLIPTIC-RA12H': {'point_source': ptsrc_catalog,
#                               'galaxy': 'none',
#                               'moving_pointsource': mt_cat},
#             'ECLIPTIC-RA0H': {'point_source': 'none'}
#             }

background = 'high'
output_dir = '/arc/projects/classy/MarsSandbox/mirage0/mirage_input_files/yaml_files/sim_obs'
simulation_dir = '/arc/projects/classy/MarsSandbox/mirage0/mirage_input_files/sim_data/sim_obs'
datatype = 'raw'
roll_angle = 291.0
dates = {'001': '2023-01-24', '002': '2023-01-29', '003': '2023-02-03', '004': '2023-01-24', '005': '2023-01-29', '006': '2023-02-03'}
# cr = {'library': 'SUNMAX', 'scale': 0.}

# reffile_overrides = {'nircam': {'superbias':    {'nrcb5': {'bright1': None},
#                                                  'nrcb4': {'bright1': None},
#                                                  'nrcb3': {'bright1': None},
#                                                  'nrcb2': {'bright1': None},
#                                                  'nrcb1': {'bright1': None},
                                                 
#                                                  'nrca5': {'bright1': None},
#                                                  'nrca4': {'bright1': None},
#                                                  'nrca3': {'bright1': None},
#                                                  'nrca2': {'bright1': None},
#                                                  'nrca1': {'bright1': None}
#                                                 },
#                                'linearized_darkfile':    {'nrcb5': '/arc/projects/classy/MarsSandbox/mirage0/mirage_input_files/sim_data/jw01568002013_01101_00026_nrcb5_uncal_linear_dark_prep_object.fits'}
#                                }
#                     }

yam = yaml_generator.SimInput(input_xml=xml_file, pointing_file=pointing_file,
                              catalogs=cat_dict,
                              roll_angle=roll_angle,
                              dates=dates,
                              background=background,
                              verbose=True, output_dir=output_dir,
                              simdata_output_dir=simulation_dir,
                              datatype=datatype)
                              # cosmic_rays=cr)
                              # reffile_overrides=reffile_overrides)

yam.create_inputs()