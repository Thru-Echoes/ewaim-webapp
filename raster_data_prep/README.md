# Raster data preperation

This folder contains raster data preparation utilities function. Before doing anything, please unzip the `pearl_data.zip` file.

## Requirements

This utility function requires `gdal` and `R` with library `raster`. The reason why `R` is needed is because the raw data are `R rasters`. 

To use these data, I need to use `R` to convert the data to `GeoTIFF` first, and then use `gdal` for further preparation. 

To install `gdal` for OSX:

```bash
  brew install gdal
```

To install `R`, go to this [link](https://www.r-project.org/). When `R` is installed, in R, type:

```R
  install.package('raster')
```

## Use

When you have all the dependencies installed, use:

```bash
  python raster_translation.py
```
