# My notes about Google Earth Engine (using Python)
I will commit here some code and notes. This is not a tutorial of Google Earth Engine.

## Download
To export/download data, in my case raster data (ee.Image), to your computer from Earth Engine you 
can use either **ee.Image.getDownloadURL** method [[1]](https://developers.google.com/earth-engine/apidocs/ee-image-getdownloadurl)
[[2]](https://github.com/gee-community/qgis-earthengine-plugin/blob/master/examples/download_by_canvas.py), 
or do it via exporting data to your **Google Drive**. [[3](https://developers.google.com/earth-engine/guides/exporting)]
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

Simple example of using getDownloadURL is in [download_sen1_getDownloadURL_one_image.py](https://github.com/CzendaZdenda/google-earth-engine-notes/blob/main/download_sen1_getDownloadURL_one_image.py). Most interesting part is this:
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

__Some limitations of getDownloadURL__

_ee.ee_exception.EEException: Pixel grid dimensions (...x...) must be less than or equal to 10000._

_ee.ee_exception.EEException: Total request size (... bytes) must be less than or equal to 33554432 bytes._


### toDrive

Images will be exported to your Google Drive folder (toDrive). Then you can download it.

You can check tasks in [Code Editor](https://code.earthengine.google.com/) in the Tasks tab. There you can also check errors etc.

__Some limitations of toDrive__

Error: Export too large: specified 598674825 pixels (max: 100000000). Specify higher maxPixels value if you intend to export a large area.

Error: Export too large: specified 598674825 pixels (max: 100000000). Specify higher maxPixels value if you intend to export a large area.

-> clip by some area (use parameter 'region')

-> use a higher value of 'scale' parameter, maybe you don't need so detailed resolution

Error: Exported bands must have compatible data types; found inconsistent types: Float64 and Float32.

-> Because of "... Currently only 'GeoTIFF' and 'TFRecord' are supported, defaults to 'GeoTIFF'..." and 
in GeoTIFF you can not mix data types. Try to save bands separately (use image.select('band_name')). 

## Plotting Timeseries
TODO
