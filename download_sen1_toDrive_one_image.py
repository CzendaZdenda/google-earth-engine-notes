# -*- coding: utf-8 -*-
#
#   Download one image of Sentinel-1 SAR GRD dataset [1] using ee.batch.Export.image.toDrive() method.
#
#   [1] https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD

import ee
import time


def main():
    # uncomment this in case you did not authenticate to Earth Engine yet
    # ee.Authenticate()

    # initialize ee library
    ee.Initialize()

    dataset_name = 'COPERNICUS/S1_GRD'

    # Moravia
    filename = 'S1A_IW_GRDH_1SDV_20191211T050136_20191211T050201_030296_037700_8DB5'
    scale = 10

    # Pribor
    region = ee.Geometry.Polygon([[17.9736328125, 49.41276017251568],
                                  [18.52020263671875, 49.41276017251568],
                                  [18.52020263671875, 49.84860975344834],
                                  [17.9736328125, 49.84860975344834],
                                  [17.9736328125, 49.41276017251568]])

    pol = ['VV']

    short_name = f"{'_'.join(filename.split('_')[:-3])}_{''.join(pol)}_{scale}m"
    image = ee.Image(f"{dataset_name}/{filename}")

    # scale is in meters
    task = ee.batch.Export.image.toDrive(
        image=image.select(pol),
        description=short_name,
        folder='earth_engine_test',
        region=region,
        # maxPixels=1e9,
        scale=scale)

    task.start()

    while task.active():
        print('Polling for task (id: {}).'.format(task.id))
        time.sleep(5)

    task_status = task.status()
    print(task_status['state'])
    if task_status['state'] == task.State.FAILED:
        print(task_status['error_message'])


if __name__ == '__main__':
    main()
