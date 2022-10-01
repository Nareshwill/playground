var events = require("events");
var eventEmitter =  new events.EventEmitter();

var connectHandler = function connected() {
    console.log("connected");
    eventEmitter.emit("data_received");
};

eventEmitter.on("data_received", function(){
    console.log("data received");
})

eventEmitter.emit("connection");
console.log("Program Ended")



console.log("This is first");
setImmediate(function() {
    console.log("This is seciond");
})
console.log("this is third")


function async(arg, callback) {
    console.log(`do someting with ${arg}`);
    setTimeout(function() { callback(arg*2); }, 1000);
}

var items = [1, 2, 3, 4, 5, 6];
var results = [];
function series(item) {
    if(item) {
        async(item, function(result) {
            results.push(result);
            return series(items.shift());
        })
    }
}

series(items.shift());


var buffer1 = new Buffer("India");
var buffer2 = new Buffer();
buffer1.copy(buffer2);
console.log("buffer2 content: "  + buffer2.toString());