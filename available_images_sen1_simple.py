# -*- coding: utf-8 -*-
#
#   Get some information about images, that are available over your area.
#
#   In this example the "COPERNICUS/S1_GRD" dataset (Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar Ground
# Range Detected, log scaling) is used [1].
#
# [1] https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD

import ee


def main():
    # uncomment in case you did not authenticate to Earth Engine yet
    # ee.Authenticate()

    # initialize ee library
    ee.Initialize()

    # define an area of interest (eg. Chara Sands)
    region = ee.Geometry.Polygon(
        [[118.06, 56.81],
         [118.21, 56.81],
         [118.21, 56.88],
         [118.06, 56.88],
         [118.06, 56.81]])

    # set dataset
    dataset_name = "COPERNICUS/S1_GRD"

    sen_collection = ee.ImageCollection(dataset_name) \
        .filterBounds(region)

    collection_info = sen_collection.getInfo()

    for k in collection_info["features"]:
        properties = k['properties']

        ori_filename = properties['system:index']
        res_m = properties['resolution_meters']
        pol = properties['transmitterReceiverPolarisation']
        plat = properties['platform_number']
        plat_name = properties['familyName']
        orbit = properties['orbitProperties_pass']
        mode = properties['instrumentMode']

        print(f'{ori_filename}, {res_m}m, {pol}, {plat_name}{plat}, {orbit}, {mode}')


if __name__ == '__main__':
    main()
