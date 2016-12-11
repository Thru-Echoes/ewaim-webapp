# Use XGB binary prediction model on raster data

rasterXgb <- function(xgbModel, rData, nLayers) {

    for (i in 1:nLayers) {
        rastPred[i,] <- predict(xgbModel, rData[i,], missing=NA)
        print("Current rasterXgb loop iteration: ", i)
    }
}
