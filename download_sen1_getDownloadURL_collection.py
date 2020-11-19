# -*- coding: utf-8 -*-
#
#    Download Sentinel-1 SAR GRD dataset collection[1] using ee.Image.getDownloadURL() method. Clipped by an area.
#  Filtered by date, bounds(region, area), platform_number ('A' for Sentinel-1A, 'B' for Sentinel-1B),
#  orbitProperties_pass (ASCENDING, DESCENDING), instrumentMode (IW, EW, SM), resolution_meters (10, 25, 40) and
#  polarization (['VV'], ['VV', 'VH'], ['HH'], ['HV']).
#
#    In this example a spatial resolution of the images is 10 metres. I set scale parameter to 40 metres, because
#  the getDownloadURL approach is limited by the total request size, which must be less than or equal to 33554432 bytes
#  (~33.5 MB).
#
#  [1] https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD

import ee
import requests
from pathlib import Path


def main():
    # uncomment this in case you did not authenticate to Earth Engine yet
    # ee.Authenticate()

    # initialize ee library
    ee.Initialize()

    dataset_name = 'COPERNICUS/S1_GRD'
    dst_dir = Path('data/download/test')
    dst_dir.mkdir(parents=True, exist_ok=True)

    # Svyatoy Nos Peninsula
    region = ee.Geometry.Polygon([[108.38836669921874, 53.45044250555688],
                                  [109.171142578125, 53.45044250555688],
                                  [109.171142578125, 53.904338156274704],
                                  [108.38836669921874, 53.904338156274704],
                                  [108.38836669921874, 53.45044250555688]])

    date_from = '2019-10-01'
    date_to = '2020-05-31'
    plat = 'B'
    orbit = 'DESCENDING'
    mode = 'IW'
    pol = 'VV'
    res = 10
    scale = 40

    sen_collection = ee.ImageCollection(dataset_name) \
        .filterBounds(region) \
        .filterDate(ee.Date(date_from), ee.Date(date_to)) \
        .filter(ee.Filter.eq('orbitProperties_pass', orbit)) \
        .filter(ee.Filter.eq('instrumentMode', mode)) \
        .filter(ee.Filter.eq('resolution_meters', res)) \
        .filter(ee.Filter.eq('platform_number', plat)) \
        .filter(ee.Filter.listContains('transmitterReceiverPolarisation', pol))

    collection_info = sen_collection.getInfo()
    for k in collection_info["features"]:
        ori_filename = k['properties']['system:index']

        print(ori_filename)

        # get image
        sen_1 = ee.Image(f"{dataset_name}/{ori_filename}").select([pol, 'angle'])

        new_filename = f"{'_'.join(ori_filename.split('_')[:-3])}_clipped_{scale}m"
        url = sen_1.getDownloadURL({
            'name': new_filename,
            'scale': scale,
            'region': region
        })

        r = requests.get(url)

        if r.status_code != 200:
            print(r)
        else:
            filename = r.headers.get('Content-disposition').split(';')[1].split('=')[1]

            with open(dst_dir / filename, 'wb') as new_file:
                new_file.write(r.content)


if __name__ == '__main__':
    main()
