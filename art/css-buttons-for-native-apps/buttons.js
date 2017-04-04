var page = require('webpage').create();
var fs = require('fs');
var system = require('system')

if (system.args.length < 4) {
console.log("usage: phantomjs " + system.args[0] + " <stylesheet.css> <output.png> <buttonlabel> [<buttonclass>]")
phantom.exit(1);
}

var styles = fs.read(system.args[1]);
var output = system.args[2];
var label = system.args[3];
var klass = (system.args.length > 4) ? system.args[4] : "";

page.content = '<html><head><style type="text/css"></style></head><body><span><button></button></span></body></html>';

page.clipRect = page.evaluate(function(styles, label, klass) {

    document.getElementsByTagName('style')[0].textContent = styles;

    var button = document.getElementsByTagName('button')[0];
    button.textContent = label;
    button.className = klass;

    return {
        top:     button.offsetTop,
        left:    button.offsetLeft,
        width:   button.offsetWidth,
        height:  button.offsetHeight
    }
}, styles, label, klass);

page.render(output);

phantom.exit();
