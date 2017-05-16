var gpio = require('rpi-gpio');
 
gpio.setup(40, gpio.DIR_OUT, write);
 
function write() {
    gpio.write(40, false, function(err) {
        if (err) throw err;
        console.log('Written to pin');
    });
}
