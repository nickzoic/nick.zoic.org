---
category: etc
date: '2014-01-01'
layout: article
redirect_from: '/etc/css-buttons-for-native-apps/'
slug: 'css-buttons-for-native-apps'
summary: 'Using CSS to make nice looking buttons for Native Apps (using PhantomJS)'
tags:
    - css
    - ios
    - android
title: CSS Buttons for Native Apps
---

A client was complaining to me the other day that while we've got all
our HTML5 buttons under control with CSS, the buttons of his native apps
are nowhere near as easy to deal with: instead, he's got a graphic
designer tweaking each one in Photoshop, and no easy way for the
programmers to produce a new matching button on the fly.

It occurred to me that the CSS approach worked so well in the browser
that we should just steal it. There's a million [CSS Button
Generators](http://google.com/search?q=css+button+generator) out there
to help you tweak the CSS, what's needed from there is just a way to
render different text onto the buttons just like a browser would.

Thankfully, there's [PhantomJS](http://phantomjs.org/), which is a
headless WebKit browser with extra support for automation in Javascript.
You run it with a little control script which can load assets and render
into a file and so on. It's actually very flexible.

Here what I've got it doing is applying your CSS to an html `<button>`
element, then cropping that button out of the page and dumping it to a
file.

The control script, `buttons.js`, looks like this:

``` {.sourceCode .javascript}
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
```

To make a "Fnord" button with your `my_buttons.css` file, run:

    phantomjs buttons.js my_buttons.css button_fnord.png Fnord

If you want to have many button styles in the one css file, you can give
each style its own CSS class and pass the CSS class name on the command
line too.

You could easily add these as Makefile rules, for example:

``` {.sourceCode .makefile}
buttons/save.png: my_buttons.css
    phantomjs buttons.js $< $@ Save save

buttons/cancel.png: my_buttons.css
    phantomjs buttons.js $< $@ Cancel cancel
```

The PNG files will get rebuilt by Make any time the CSS file changes.

PS: This code is obviously pretty sketchy, but you get the idea. Get to
it and think of more uses for PhantomJS!
