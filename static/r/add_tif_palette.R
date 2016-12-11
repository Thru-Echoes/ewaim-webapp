# From: http://rstudio-pubs-static.s3.amazonaws.com/3334_35452e4a611a4fa39ccebd26dffe4c9e.html

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

# writePaletteVRT("test.vrt", r, rainbow(6))
