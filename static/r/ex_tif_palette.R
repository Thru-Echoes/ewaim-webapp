library(raster)

test <- function(r_dir) {
  r <- raster(r_dir)
  r[r != 1] <- NA
  setwd()
  writeRaster(r, gsub(".grd", ".tif", r_dir), format="GTiff")
  setwd(r_dir)
}

abba_root_path = "~/Documents/research-projects/main/ewaim-webapp/static/data/pearl-tif/pearl_data/abbreviata_bancrofti/"
abba_file_path = paste(abba_root_path, "grd/ABBREVIATA BANCROFTI current.grd", sep = "")
abba_tif_path = paste(abba_root_path, "tif/ABBREVIATA BANCROFTI current.tif", sep = "")
abba_tif_dir = paste(abba_root_path, "tif/", sep = "")

abba_raster = raster(abba_file_path)
abba_raster[abba_raster != 1] = NA
#setwd(abba_tif_path)
writeRaster(abba_raster, gsub("grd", "tif", abba_file_path), format="GTiff")
#setwd(r_dir)


######

makePalette <- function(colourvector) {
    cmat = cbind(t(col2rgb(colourvector)), 255)
    res = apply(cmat, 1, function(x) {
        sprintf("<Entry c1=\"%s\" c2=\"%s\" c3=\"%s\" c4=\"%s\"/>", x[1], x[2],
            x[3], x[4])
    })
    res = paste(res, collapse = "\n")
    res
}

makePaletteVRT <- function(raster, colourvector) {
    s = sprintf("<VRTDataset rasterXSize=\"%s\" rasterYSize=\"%s\">\n<VRTRasterBand dataType=\"Byte\" band=\"1\">\n<ColorInterp>Palette</ColorInterp>\n<ColorTable>\n",
        ncol(raster), nrow(raster))
    p = makePalette(colourvector)
    s = paste0(s, p, "\n</ColorTable>\n</VRTRasterBand>\n</VRTDataset>\n")
    s
}

writePaletteVRT <- function(out, raster, colourvector) {
    s = makePaletteVRT(raster, colourvector)
    cat(s, file = out)
}


#####
#setwd(abba_tif_dir)
writePaletteVRT(paste(abba_tif_dir, "ABBREVIATA BANCROFTI current.vrt", sep=""), abba_raster, rainbow(5))

py_path = "~/Documents/research-projects/main/ewaim-webapp/static/py/add_tif_palette.py"
palette_run = paste(py_path, " ABBREVIATA BANCROFTI current.vrt", "ABBREVIATA BANCROFTI current.tif", sep = "")

system(palette_run)


# python add_tif_palette.py ../../static/data/pearl-tif/pearl_data/abbreviata_bancrofti/tif/ABBREVIATA\ BANCROFTI\ current.vrt ../../static/data/pearl-tif/pearl_data/abbreviata_bancrofti/tif/ABBREVIATA\ BANCROFTI\ current.tif 