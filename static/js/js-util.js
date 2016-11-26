/* Enhanced debugger for Javascript - checks type better */

// Enhanced error checking (GLOBAL)
var isType = function(obj) {
    return ({}).toString.call(obj).match(/\s([a-zA-Z]+)/)[1].toLowerCase();
};
