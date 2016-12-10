
files_dirs = dir(path = ".", full.names = FALSE, recursive = FALSE, all.files = FALSE, no.. = FALSE)
home_dir = getwd()


abb_ban = files_dirs[1]
asc_lon = files_dirs[2]
abb_ban_path = paste(home_dir, "/", files_dirs[1], "/", "grd", sep = "")
asc_lon_path = paste(home_dir, "/", files_dirs[2], "/", "grd", sep = "")
abb_ban_tiff_path

test <- function(r_dir) {
  r <- raster(r_dir)
  r[r != 1] <- NA
  setwd()
  writeRaster(r, gsub(".grd", ".tif", r_dir), format="GTiff")
  setwd(r_dir)
}

# First pdw to raster dir
# loop through the files in the dir for the convertion
# in the convertion, set the output dir to tif folder
# test("~/my_rasters")

r_dir = abb_ban_path
r = raster(r_dir)