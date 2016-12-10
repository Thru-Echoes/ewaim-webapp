function style(feature) {
    return {
        /* fillColor: getColor(feature.properties.density), */
        fillColor: "purple",
        fillOpacity: 0.2,
        weight: 5,
        opacity: 0.8,
        color: '#000',
        dashArray: '3',
    };
}

function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#000',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
    state_info.state_update(layer.feature.properties);
}

function resetHighlight(e) {
    states_layer.resetStyle(e.target);
    state_info.state_update();
}

function zoomToFeature(e) {
    map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
    layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
    });
}

/* */

function point_feature(e) {
    var layer = e.target;
    point_info.point_update(layer.feature.properties);
}

function point_reset(e) {
    point_info.point_update();
}

function point_on(feature, p_layer) {
    layer.on({
        mouseover: point_feature,
        mouseout: point_reset,
    });
}
