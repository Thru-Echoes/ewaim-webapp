# 24 June - R: how to turn GRD into SHP / TIFF / Image 
library(sp)
library(rgdal)
library(raster)
cont <- readOGR(dsn = path.expand('abco/'), layer = 'cont')
abco.current <- raster('abco/ABBREVIATA CONFUSA current.grd')
abco.ac45 <- raster('abco/ABBREVIATA CONFUSA futureac45.grd')
abco.ac85 <- raster('abco/ABBREVIATA CONFUSA futureac85.grd')

par(oma = c(0, 0, 0, 0), mar = c(0, 0, 0, 0))

plot(abco.current,xaxt='n',yaxt='n',legend=FALSE)
plot(cont,xaxt='n',yaxt='n',add=TRUE)

plot(abco.ac45,xaxt='n',yaxt='n',legend=FALSE)
plot(cont,xaxt='n',yaxt='n',add=TRUE)

plot(abco.ac85,xaxt='n',yaxt='n',legend=FALSE)
plot(cont,xaxt='n',yaxt='n',add=TRUE)
