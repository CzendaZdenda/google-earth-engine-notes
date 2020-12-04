# -*- coding: utf-8 -*-
#
#   Get timeseries Sentinel-1 data for a given point. Inspired by [1]
#
#   In this example the "COPERNICUS/S1_GRD" dataset (Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar Ground
# Range Detected, log scaling) is used [1].
#
# [1] https://developers.google.com/earth-engine/tutorials/community/time-series-visualization-with-altair
# [2] https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD

import ee
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


# uncomment in case you did not authenticate to Earth Engine yet
# ee.Authenticate()

# initialize ee library
ee.Initialize()

EPOCH_START = datetime(1970, 1, 1)


def create_reduce_region_function(geometry,
                                  reducer=ee.Reducer.mean(),
                                  scale=1000,
                                  crs='EPSG:4326',
                                  bestEffort=True,
                                  maxPixels=1e13,
                                  tileScale=4):
    """Creates a region reduction function.

    Creates a region reduction function intended to be used as the input function
    to ee.ImageCollection.map() for reducing pixels intersecting a provided region
    to a statistic for each image in a collection. See ee.Image.reduceRegion()
    documentation for more details.

    Getting from https://developers.google.com/earth-engine/tutorials/community/time-series-visualization-with-altair.

    Args:
    :param geometry:    An ee.Geometry that defines the region over which to reduce data.
    :type geometry:     ee.Geometry

    :param reducer:     An ee.Reducer that defines the reduction method. Optional.
    :type reducer:      ee.Reducer

    :param scale:       A number that defines the nominal scale in meters of the projection to work in. Optional.
    :type scale:        int

    :param crs:         An ee.Projection or EPSG string ('EPSG:5070') that defines the projection to work in. Optional.
    :type crs:          ee.Projection | str

    :param bestEffort:  A Boolean indicator for whether to use a larger scale if the geometry contains too many pixels
                        at the given scale for the operation to succeed. Optional.
    :type bestEffort:   bool

    :param maxPixels:   A number specifying the maximum number of pixels to reduce. Optional.
    :type maxPixels:    int

    :param tileScale:   A number representing the scaling factor used to reduce aggregation tile size; using a larger
                        tileScale (e.g. 2 or 4) may enable computations that run out of memory with the default.
                        Optional.
    :type tileScale:    int

    :return:            A function that accepts an ee.Image and reduces it by region, according to the provided
                        arguments.
    :rtype:             function
    """

    def reduce_region_function(img):
        """Applies the ee.Image.reduceRegion() method.

        :param img:     An ee.Image to reduce to a statistic by region.
        :type img:      ee.Image

        :return:        An ee.Feature that contains properties representing the image region reduction results per band
                        and the image timestamp formatted as milliseconds from Unix epoch (included to enable time
                        series plotting).
        :rtyp:          ee.Feature
        """

        stat = img.reduceRegion(
            reducer=reducer,
            geometry=geometry,
            scale=scale,
            crs=crs,
            bestEffort=bestEffort,
            maxPixels=maxPixels,
            tileScale=tileScale)

        return ee.Feature(geometry, stat).set({'millis': img.date().millis()})
    return reduce_region_function


def fc_to_dict(fc):
    """ Define a function to transfer feature properties to a dictionary.

    Getting from https://developers.google.com/earth-engine/tutorials/community/time-series-visualization-with-altair.

    :param fc:      Collection of features to be transfer to a ee.Dictionary.
    :type fc:       ee.FeatureCollection

    :return:        ee.Dictionary representation of a given feature colelction.
    :rtype:         ee.Dictionary
    """
    # ee.ee_list.List - eg. prop_names.getInfo() -> ['system:index', 'HH', 'HV', 'angle']
    prop_names = fc.first().propertyNames()
    prop_lists = fc.reduceColumns(
        reducer=ee.Reducer.toList().repeat(prop_names.size()),
        selectors=prop_names).get('list')

    return ee.Dictionary.fromLists(prop_names, prop_lists)


def main():
    dataset_name = 'COPERNICUS/S1_GRD'

    date_from = ee.Date('2017-01-01')
    date_to = ee.Date('2020-12-31')
    plat = 'B'
    orbit = 'DESCENDING'
    mode = 'IW'
    res = 10
    pol = ['VV', 'VH']

    # filter of 3x3 mask
    kernel_3x3 = ee.Kernel.square(radius=1)

    # Chara sands
    point = ee.Geometry.Point(118.133761, 56.840481)

    sen_collection = ee.ImageCollection(dataset_name) \
        .filterDate(date_from, date_to) \
        .filterBounds(point.buffer(1000)) \
        .filter(ee.Filter.eq('platform_number', plat)) \
        .filter(ee.Filter.eq('orbitProperties_pass', orbit)) \
        .filter(ee.Filter.eq('instrumentMode', mode)) \
        .filter(ee.Filter.eq('resolution_meters', res)) \
        .filter(ee.Filter.eq('transmitterReceiverPolarisation', pol)) \
        .map(lambda img: img.convolve(kernel_3x3).convolve(kernel_3x3))

    reduce_fc = create_reduce_region_function(point, scale=res)

    data_fc = ee.FeatureCollection(sen_collection.map(reduce_fc)).filter(
        ee.Filter.notNull(sen_collection.first().bandNames()))

    data_dict = fc_to_dict(data_fc).getInfo()

    data = pd.DataFrame(data_dict)
    data['date'] = data['millis'].apply(lambda row: EPOCH_START + timedelta(milliseconds=row))
    col_names = data.columns.tolist()
    col_names.remove('millis')
    data = data[col_names].set_index('date')

    # PLOT ANGLE vs dB
    fig = plt.figure(num='ai_vs_db', constrained_layout=True)
    ax = fig.add_subplot()

    ax.plot(data['angle'], data['VV'], '.', label='VV')
    ax.plot(data['angle'], data['VH'], '.', label='VH')

    ax.set_xlabel('angle')
    ax.set_ylabel('[dB]')
    ax.legend()

    # PLOT TIMESERIE
    fig = plt.figure(num='ts', constrained_layout=True, figsize=(12, 6))
    ax = fig.add_subplot()

    data_i = data.loc[(data.angle >= 39.55) & (data.angle <= 39.57)]

    ax.plot(data_i.index, data_i['VV'], '.-', label='VV <39.55, 39.57>')
    ax.plot(data_i.index, data_i['VH'], '.-', label='VH <39.55, 39.57>')

    ax.set_xlabel('Date')
    ax.set_ylabel('[dB]')
    ax.legend()

    plt.show()


if __name__ == '__main__':
    main()
