# -*- coding: utf-8 -*-
#
#   In this example the "COPERNICUS/S1_GRD" dataset (Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar Ground
# Range Detected, log scaling) is used [1].
#
# [1] https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD

import ee


def just_region_filtering():
    # uncomment in case you did not authenticate to Earth Engine yet
    # ee.Authenticate()

    # initialize ee library
    ee.Initialize()

    # define an area of interest
    region = ee.Geometry.Polygon(
        [[118.06526184082031, 56.81102820967043],
         [118.20945739746094, 56.81102820967043],
         [118.20945739746094, 56.881062658158335],
         [118.06526184082031, 56.881062658158335],
         [118.06526184082031, 56.81102820967043]])

    # set dataset
    dataset_name = "COPERNICUS/S1_GRD"

    sen_collection = ee.ImageCollection(dataset_name) \
        .filterBounds(region)

    collection_info = sen_collection.getInfo()

    for k in collection_info["features"]:
        ori_filename = k['properties']['system:index']
        res_m = k['properties']['resolution_meters']
        pol = k['properties']['transmitterReceiverPolarisation']
        print(f'{ori_filename}: {res_m}, {pol}')


def main():
    just_region_filtering()

    return
    # uncomment in case you did not authenticate to Earth Engine yet
    # ee.Authenticate()

    # initialize ee library
    ee.Initialize()

    # define an area of interest
    region = ee.Geometry.Polygon(
        [[118.06526184082031, 56.81102820967043],
         [118.20945739746094, 56.81102820967043],
         [118.20945739746094, 56.881062658158335],
         [118.06526184082031, 56.881062658158335],
         [118.06526184082031, 56.81102820967043]])

    # set
    # date_from_str = date(2019, 12, 1)
    # date_to_str = date(2019, 12, 31)
    dataset_name = "COPERNICUS/S1_GRD"
    # plat = 'B'
    # orbit = 'DESCENDING'
    # mode = 'IW'
    # res = 10

    sen_collection = ee.ImageCollection(dataset_name) \
        .filterDate(date_from_str, date_to_str) \
        .filterBounds(region)  # \
    # .filter(ee.Filter.eq('platform_number', plat)) \
    # .filter(ee.Filter.eq('orbitProperties_pass', orbit)) \
    # .filter(ee.Filter.eq('instrumentMode', mode)) \
    # .filter(ee.Filter.eq('resolution_meters', res))


if __name__ == '__main__':
    main()
