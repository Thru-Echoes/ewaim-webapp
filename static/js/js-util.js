/* Enhanced debugger for Javascript - checks type better */
var is_type = function(obj) {
    return ({}).toString.call(obj).match(/\s([a-zA-Z]+)/)[1].toLowerCase();
};

var map_util = {
    version: "0.0.1",
    get_map: function() {
        print("Oh like skrrt");
        return console.log("Like skrrt");
    },
};

/* Twitter data utility function for counties (is Python) */
/*tweets = []

for county, _ in results:

    cursor.execute(""" SELECT ST_AsGeoJSON(tw.location)
                       FROM k_tweets tw, ca_census_tract ce
                       WHERE ST_Within(tw.location, ce.geom)=true
                       AND ce.name10='%s'; """ % county)

    tweets.append([county, cursor.fetchall()]) */
