# My notes about Google Earth Engine (using Python)
I will commit here some code and notes. This is not a tutorial of Google Earth Engine.

[Links](https://github.com/CzendaZdenda/google-earth-engine-notes#links)

[How to get information about available files within an area?](https://github.com/CzendaZdenda/google-earth-engine-notes#how-to-get-information-about-available-files-within-an-area)

[Download](https://github.com/CzendaZdenda/google-earth-engine-notes#download)

[Download collection (Sentinel-1)](https://github.com/CzendaZdenda/google-earth-engine-notes#download-clipped-images-over-some-area-within-some-period-sentinel-1)

---

## Links
[Official examples on GitHub](https://github.com/google/earthengine-api/tree/master/python)

[Export data (Colaboratory)](https://colab.research.google.com/github/csaybar/EEwPython/blob/dev/10_Export.ipynb#scrollTo=M9EbU74_ESvY)

[Export data (GEE)](https://developers.google.com/earth-engine/guides/exporting)

[geojson.io](https://geojson.io/#map=9/53.6536/108.6383)
Easy way to get coordinates in GeoJSON format.

## How to get information about available files within an area? 

Simple example of getting information about available Sentinel-1 data is in [available_images_sen1_simple.py](https://github.com/CzendaZdenda/google-earth-engine-notes/blob/master/available_images_sen1_simple.py).

First define a region:
```python
region = ee.Geometry.Polygon(
        [[118.06526184082031, 56.81102820967043],
         [118.20945739746094, 56.81102820967043],
         [118.20945739746094, 56.881062658158335],
         [118.06526184082031, 56.881062658158335],
         [118.06526184082031, 56.81102820967043]])
```

Here is an example how to create 100m x 100m rectangle around a point:
```python
# ee.Geometry.Point([lon, lat])
rect = ee.Geometry.Point([118.134323, 56.839642]).buffer(100/2).bounds()
```  

Than get a collection of images and filter by you area:
```python
sen_collection = ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(region)
```

You can also filter by date or another parameters:
```python
sen_collection = ee.ImageCollection("COPERNICUS/S1_GRD") \
        .filterDate('2019-12-1', '2019-12-31') \
        .filterBounds(region)  \
        .filter(ee.Filter.eq('platform_number', 'B')) \
        .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING')) \
        .filter(ee.Filter.eq('instrumentMode', 'IW')) \
        .filter(ee.Filter.eq('resolution_meters', 10))
```

Parameters like 'platform_number' etc. are properties of Sentinel-1 dataset. More you can get [here](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD) in Image Properties part.  
Using `sen_collection.getInfo()` (method of ee.ImageCollection) you will get information of collection in a dictionary format.
If you want get information of Images (not Collection), you can use 'feature'-key (`sen_collection.getInfo()["features"]`) to get list of dictionaries with information for each image/feature.

Information for each image looks like this:
```python
{
    "type": "Image",
    "bands": [
        {
            "id": "VV",
            "data_type": {"type": "PixelType", "precision": "double"},
            "dimensions": [29644, 22018],
            "crs": "EPSG:32634",
            "crs_transform": [10, 0, 190615.1700898306, 0, -10, 5568907.024637105],
        },
        {
            "id": "VH",
            "data_type": {"type": "PixelType", "precision": "double"},
            "dimensions": [29644, 22018],
            "crs": "EPSG:32634",
            "crs_transform": [10, 0, 190615.1700898306, 0, -10, 5568907.024637105],
        },
        {
            "id": "angle",
            "data_type": {"type": "PixelType", "precision": "float"},
            "dimensions": [21, 10],
            "crs": "EPSG:32634",
            "crs_transform": [
                13123.153716519882,
                -2997.124020510295,
                224484.88563284784,
                1943.6171710630879,
                20154.351669282652,
                5355371.242224661,
            ],
        },
    ],
    "id": "COPERNICUS/S1_GRD/S1A_IW_GRDH_1SDV_20191202T163455_20191202T163520_030172_0372A4_67BA",
    "version": 1605770302269949,
    "properties": {
        "GRD_Post_Processing_start": 1575312426960,
        "sliceNumber": 13,
        "GRD_Post_Processing_facility_name": "Copernicus S1 Core Ground Segment - DPA",
        "resolution": "H",
        "SLC_Processing_facility_name": "Copernicus S1 Core Ground Segment - DPA",
        "system:footprint": {
            "type": "LinearRing",
            "coordinates": [
                [20.650383724905083, 48.683636829205376],
                [20.708093752413863, 48.689462042765875],
                [20.692741981351944, 48.77453832068133],
                [20.61576122666991, 49.1229831381155],
                [20.532279753481006, 49.47321860393239],
                [20.356153119714357, 50.16503175299044],
                [20.35020201925955, 50.186220664724914],
                [19.23253684554866, 50.07195252769796],
                [18.433621274536364, 49.98332788323961],
                [17.917943794094278, 49.92302405181339],
                [17.006240203032174, 49.81041382117267],
                [16.899647073277396, 49.79672408245612],
                [16.906379196953758, 49.75661742731832],
                [16.908261475308446, 49.74912228054839],
                [16.912415470888412, 49.734420467927706],
                [17.022557803424927, 49.37626305205186],
                [17.130959415106226, 49.017945702798535],
                [17.23766868030927, 48.65947158203902],
                [17.343143252770933, 48.29943020529188],
                [17.346405753633135, 48.299534017246586],
                [20.650383724905083, 48.683636829205376],
            ],
        },
        "familyName": "SENTINEL-1",
        "segmentStartTime": 1575304191900,
        "missionDataTakeID": 225956,
        "GRD_Post_Processing_facility_country": "Germany",
        "nssdcIdentifier": "2014-016A",
        "productClass": "S",
        "phaseIdentifier": 1,
        "orbitProperties_pass": "ASCENDING",
        "relativeOrbitNumber_stop": 175,
        "system:time_end": 1575304495000,
        "SLC_Processing_facility_site": "DLR-Oberpfaffenhofen",
        "GRD_Post_Processing_stop": 1575313120000,
        "system:time_start": 1575304495000,
        "instrumentMode": "IW",
        "totalSlices": 29,
        "SLC_Processing_stop": 1575312891000,
        "startTimeANX": 789446.6,
        "SLC_Processing_start": 1575312553000,
        "resolution_meters": 10,
        "instrumentSwath": "IW",
        "relativeOrbitNumber_start": 175,
        "productTimelinessCategory": "Fast-24h",
        "SLC_Processing_software_name": "Sentinel-1 IPF",
        "sliceProductFlag": "true",
        "S1TBX_Calibration_vers": "6.0.4",
        "orbitNumber_start": 30172,
        "GRD_Post_Processing_facility_site": "DLR-Oberpfaffenhofen",
        "instrument": "Synthetic Aperture Radar",
        "GRD_Post_Processing_software_name": "Sentinel-1 IPF",
        "platform_number": "A",
        "S1TBX_SAR_Processing_vers": "6.0.4",
        "productType": "GRD",
        "orbitProperties_ascendingNodeTime": 1575303706150,
        "stopTimeANX": 814445.5,
        "productComposition": "Slice",
        "productClassDescription": "SAR Standard L1 Product",
        "GRD_Post_Processing_software_version": "003.10",
        "SLC_Processing_software_version": "003.10",
        "orbitNumber_stop": 30172,
        "instrumentConfigurationID": 6,
        "system:asset_size": 4063225529,
        "cycleNumber": 186,
        "system:index": "S1A_IW_GRDH_1SDV_20191202T163455_20191202T163520_030172_0372A4_67BA",
        "SNAP_Graph_Processing_Framework_GPF_vers": "6.0.4",
        "SLC_Processing_facility_org": "ESA",
        "SLC_Processing_facility_country": "Germany",
        "GRD_Post_Processing_facility_org": "ESA",
        "transmitterReceiverPolarisation": ["VV", "VH"],
    },
}
```
If talking about Sentinel-1 data I usually need information about orbit(ascending, descending), mode (IW, EW, SM) 
and polarization (['VV'], ['HH'], ['VV', 'VH'], or ['HH', 'HV']). `system:footprint` parameter could be also interesting,
for example for checking how much the image cross your area.  

With this you can filter those images you need for the next work.

If you are familier with [Earth Engine Code Editor](https://code.earthengine.google.com/), you can easily add image(s) into a map:
```javascript
var image=ee.Image('COPERNICUS/S1_GRD/S1A_IW_GRDH_1SDH_20161207T094531_20161207T094556_014272_017165_B235');

Map.addLayer(image.select(['HH']), {opacity: 0.5});
Map.setCenter(118.134323, 56.839642, 6);
```
And check if it is located where you think.

## Download
To export/download data, in my case raster data (ee.Image), to your computer from Earth Engine you 
can use either **ee.Image.getDownloadURL** method [[1]](https://developers.google.com/earth-engine/apidocs/ee-image-getdownloadurl)
[[2]](https://github.com/gee-community/qgis-earthengine-plugin/blob/master/examples/download_by_canvas.py), 
or do it via exporting data to your **Google Drive** [[3](https://developers.google.com/earth-engine/guides/exporting)]
[[4](https://colab.research.google.com/github/csaybar/EEwPython/blob/dev/10_Export.ipynb)]. 
The last method seems to be the recommended one. Otherwise, the getDownloadURL looks simpler, and if you don't need too big
image it's enough.

### ee.Image.getDownloadURL
I have read, that this is an older way to download data from Earth Engine. And maybe it 
could be unstable. Looks like that for small images works fine. Pixel grid dimensions must be less than or equal to 10000,
total request size must be less than or equal to 33554432 bytes.

Sentinel-1 data have a spatial resolution 10, 25 or 40 metres. It means, that 10000 px = 100km/250km/400km.
If we can use getDownloadURL for bigger areas, we can use the 'scale' parameter in getDownloadURL. Or rescale 
an image before getDownloadURL.

Simple example of using getDownloadURL is in [download_sen1_getDownloadURL_one_image.py](https://github.com/CzendaZdenda/google-earth-engine-notes/blob/master/download_sen1_getDownloadURL_one_image.py). Most interesting part is this:
```python
url = image.getDownloadURL({'scale': scale,
                            'name': short_name,
                            'region': region,
                            # 'filePerBand': False
                            })
```
Where image is ee.image.Image and region is ee.Geometry.

Then we can use request library to dowload data:
```python
r = requests.get(url, allow_redirects=True)

# you can get a filename from the response or set your own
filename_hdr = r.headers.get('Content-disposition').split(';')[1].split('=')[1]

with open(dst_dir / filename_hdr, 'wb') as new_file:
    new_file.write(r.content)
```

For more information you can type in python console `help(ee.Image.getDownloadURL)`.

Interesting parameters:
* name - _base name to use when constructing filenames_
* scale - _a default scale to use for any bands that do not specify one_
* region - _a polygon specifying a region to download_
* filePerBand - _whether to produce a different GeoTIFF per band (boolean). Defaults to true. If false, a single GeoTIFF is produced_

__Errors that can occur using getDownloadURL__

_ee.ee_exception.EEException: Pixel grid dimensions (...x...) must be less than or equal to 10000._

_ee.ee_exception.EEException: Total request size (... bytes) must be less than or equal to 33554432 bytes._


### toDrive

Images will be exported to your Google Drive folder (toDrive). Then you can download it.

Example is in [download_sen1_toDrive_one_image.py](https://github.com/CzendaZdenda/google-earth-engine-notes/blob/master/download_sen1_toDrive_one_image.py).

First, define the task:
```python
task = ee.batch.Export.image.toDrive(
        image=image.select(pol),
        description=short_name,
        folder='earth_engine_test',
        region=region,
        # maxPixels=1e9,
        scale=scale)
```
Then start the task:
```python
task.start()
```
You can check tasks in [Code Editor](https://code.earthengine.google.com/) in the Tasks tab. There you can also check errors etc.

Or you can use code in python:
```python
while task.active():
    print('Polling for task (id: {}).'.format(task.id))
    time.sleep(5)

task_status = task.status()
print(task_status['state'])
if task_status['state'] == task.State.FAILED:
    print(task_status['error_message'])
```
At the end the image should appear in Google Drive folder you specified. If folder does not exist, it will be created.

Interesting parameters:
* image - image you want to download
* scale - _The resolution in meters per pixel._
* maxPixels - _The maximum allowed number of pixels in the exported image. The task will fail if the exported region covers more pixels in the specified projection. Defaults to 100,000,000._
* region - _The lon,lat coordinates for a LinearRing or Polygon specifying the region to export._
* description - _Human-readable name of the task._
* folder - _The name of a unique folder in your Drive account to export into. Defaults to the root of the drive._
* fileNamePrefix - _The Google Drive filename for the export. Defaults to the name of the task._

__Errors that can occur__

Error: Not enough space in Google Drive (need 3.8GB for this export).

Error: Export too large: specified 598674825 pixels (max: 100000000). Specify higher maxPixels value if you intend to export a large area.

  -> just specify maxPixels parameter

  -> clip image by some area (use parameter 'region')

  -> use a higher value of 'scale' parameter, maybe you don't need so detailed resolution

Error: Exported bands must have compatible data types; found inconsistent types: Float64 and Float32.

  -> Because of "... Currently only 'GeoTIFF' and 'TFRecord' are supported, defaults to 'GeoTIFF'..." and  in GeoTIFF you can not mix data types. Try to save bands separately (use image.select('band_name')). 
  
  -> You can use float() or toFloat() in ee.Image to convert all bands to a 32-bit float ([ee.Image.float](https://developers.google.com/earth-engine/apidocs/ee-image-float)).

## Download clipped images over some area within some period (Sentinel-1)
Sometimes I want to investigate some area and I need Sentinel-1 images to be at my local computer. First I need to get a list of image names and then dowload them in for loop. If the area is not too big ([Download](https://github.com/CzendaZdenda/google-earth-engine-notes#download)) I can use `getDownloadURL` method. Another approach is to use `toDrive` method and exort data first to Google Drive folder. And then download them.

Example using getDownloadURL ([download_sen1_getDownloadURL_collection.py](https://github.com/CzendaZdenda/google-earth-engine-notes/blob/master/download_sen1_getDownloadURL_collection.py)) and toDrive ([download_sen1_toDrive_collection.py](https://github.com/CzendaZdenda/google-earth-engine-notes/blob/master/download_sen1_toDrive_collection.py)).

## Plotting Timeseries
TODO
