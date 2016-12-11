#! /usr/bin/env python
#
# Take a raster and add a palette
#
# From: http://rstudio-pubs-static.s3.amazonaws.com/3334_35452e4a611a4fa39ccebd26dffe4c9e.html
#

#  1. write an integer raster from R like this: writeRaster(r,"rint.tiff",datatype="INT1U")
#
#  2. write a palette file from R like this:  writePaletteVRT("test.vrt",r,rainbow(20))
#
#  3. run this script like this:
#      addPalette test.vrt rint.tiff
#     and it will modify rint.tiff, adding the palette.

try:
    from osgeo import gdal
except ImportError:
    import gdal

#import gdal2
import sys

def Usage():
    print('Usage: add_tif_palette.py palette_file raster_file')
    sys.exit(1)

gdal.AllRegister()
argv = gdal.GeneralCmdLineProcessor(sys.argv)
if argv is None:
    Usage()

if len(argv)!=3:
    Usage()

pal_file = argv[1]
raster_file = argv[2]

src_ds = gdal.Open(raster_file)

pal_ds = gdal.Open(pal_file)
ct = pal_ds.GetRasterBand(1).GetRasterColorTable().Clone()
src_ds.GetRasterBand(1).SetRasterColorTable(ct)

gtiff_driver = gdal.GetDriverByName('GTiff')
gtiff_driver.CreateCopy(raster_file, src_ds)
