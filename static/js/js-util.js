!function() {

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
}();
