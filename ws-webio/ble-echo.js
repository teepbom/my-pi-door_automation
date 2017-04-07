// Using the bleno module
var bleno = require('bleno');
var sleep = require('sleep');
var gpio = require('rpi-gpio');
gpio.setup(7, gpio.DIR_OUT);

var username = [];
var userpass = [];
var fs = require('fs');
var array = fs.readFileSync('user2').toString().split("\n");
for(i in array ) {
    var data = [];
    data = array[i].split("/");
    pass = data[3];
    name = data[5];
    userpass[i] = pass;
    username[i] = name;
    console.log("ID " + data[1]  + " Username " + username[i] + " Password "+userpass[i]);
} 


// Once bleno starts, begin advertising our BLE address
bleno.on('stateChange', function(state) {
    console.log('State change: ' + state);
    if (state === 'poweredOn') {
        bleno.startAdvertising('MyDevice',['12ab']);
    } else {
        bleno.stopAdvertising();
    }
});
 
// Notify the console that we've accepted a connection
bleno.on('accept', function(clientAddress) {
    console.log("Accepted connection from address: " + clientAddress);
});
 
// Notify the console that we have disconnected from a client
bleno.on('disconnect', function(clientAddress) {
    console.log("Disconnected from address: " + clientAddress);
});
 
// When we begin advertising, create a new service and characteristic
bleno.on('advertisingStart', function(error) {
    if (error) {
        console.log("Advertising start error:" + error);
    } else {
        console.log("Advertising start success");
        bleno.setServices([
            
            // Define a new service
            new bleno.PrimaryService({
                uuid : '12ab',
                characteristics : [
                    
                    // Define a new characteristic within that service
                    new bleno.Characteristic({
                        value : null,
                        uuid : '34cd',
                        properties : ['notify', 'read', 'write'],
                        // If the client subscribes, we send out a message every 1 second
                        onSubscribe : function(maxValueSize, updateValueCallback) {
                            console.log("Device subscribed");
                            this.intervalId = setInterval(function() {
                                console.log("Sending: Hi!");
                                updateValueCallback(new Buffer("Hi!"));
                            }, 1000);
                        },
                        
                        // If the client unsubscribes, we stop broadcasting the message
                        onUnsubscribe : function() {
                            console.log("Device unsubscribed");
                            clearInterval(this.intervalId);
                        },
                        
                        // Send a message back to the client with the characteristic's value
                        onReadRequest : function(offset, callback) {
                            console.log("Read request received");
                            callback(this.RESULT_SUCCESS, new Buffer("Echo: " + 
                                    (this.value ? this.value.toString("utf-8") : "")));
                        },
                        
                        // Accept a new value for the characterstic's value
                        onWriteRequest : function(data, offset, withoutResponse, callback) {
                            this.value = data ;
                            console.log('Write request: value = ' + this.value.toString("utf-8"));
			                                
			    for(i in userpass){
				if ( this.value.toString("utf-8") == userpass[i])
				{				
				  console.log ("Incomming User " +  username[i]);
				  break;					
				}
			    }
			    
			    callback(this.RESULT_SUCCESS);
                        }
 
                    })
                    
                ]
            })
        ]);
    }
});
