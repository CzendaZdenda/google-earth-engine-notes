# -*- coding: utf-8 -*-
#
#   Download one image of Sentinel-1 SAR GRD dataset [1] using ee.Image.getDownloadURL() method.
#
#   [1] https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD

import ee
import requests
from pathlib import Path

# uncomment this in case you did not authenticate to Earth Engine yet
# ee.Authenticate()

# initialize ee library
ee.Initialize()

dataset_name = 'COPERNICUS/S1_GRD'
dst_dir = Path(f'data/download')

# Baikal Lake
filename = 'S1B_IW_GRDH_1SDV_20201031T225743_20201031T225808_024063_02DBE1_DD6E'
scale = 50

# Svyatoy Nos Peninsula
region = ee.Geometry.Polygon([[108.38836669921874, 53.45044250555688],
                              [109.171142578125, 53.45044250555688],
                              [109.171142578125, 53.904338156274704],
                              [108.38836669921874, 53.904338156274704],
                              [108.38836669921874, 53.45044250555688]])

short_name = f"{'_'.join(filename.split('_')[:-3])}_clipped_{scale}m"

image = ee.Image(f"{dataset_name}/{filename}")

# scale is in meters (because of that 'COPERNICUS/S1_GRD' dataset has resolution in metres?)
url = image.getDownloadURL({'scale': scale,
                            'name': short_name,
                            'region': region,
                            # 'filePerBand': False
                            })

r = requests.get(url, allow_redirects=True)

# you can get a filename from the response or set your own
filename_hdr = r.headers.get('Content-disposition').split(';')[1].split('=')[1]

with open(dst_dir / filename_hdr, 'wb') as new_file:
    new_file.write(r.content)
