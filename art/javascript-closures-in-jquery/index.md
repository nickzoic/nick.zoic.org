---
category: HTML5
date: '2013-04-16'
layout: article
redirect_from: '/HTML5/javascript-closures-in-jquery/'
slug: 'javascript-closures-in-jquery'
tags:
    - html5
    - javascript
    - functional programming
title: Using Closures in Javascript
---

[Robin Ward](http://eviltrout.com/)'s recent blog post on [Why Discourse
uses
Ember.js](http://eviltrout.com/2013/02/10/why-discourse-uses-emberjs.html)
was interesting, as a contribution to the ongoing debate about the
[Javascript Cambrian
Explosion](http://axisofeval.blogspot.com.au/2011/04/new-cambrian-explosion.html).

However, he leads with an example:

> For example, on the bottom of every discourse post there is a button a
> user can click to like a post. When clicked, it vanishes and adds a
> footer below the post saying you liked it.
>
> If you implementing this in jQuery, you might add a data-post-id to
> the post. Then you’d bind a click event on your button element to a
> function that would make the AJAX call to the server. However, the
> click function passes a reference to the button, not the post. So you
> then have to traverse the DOM upwards to find the post the button
> belongs to and grab the id from there. Once you have it, you can make
> your XHR request. If the XHR succeeds, you then have to traverse the
> DOM downward from the post to the footer, and add in the text.
>
> At this point it works, but you’ve tied your implementation of the
> button click to a particular DOM structure. If you ever want to change
> your HTML around, you might have to adjust all the jQuery methods that
> accessed it.

I'd agree about the data-post-id kludge ... it is a horrible wart in
jQuery. However, Javascript has a much nicer way of doing these things,
using *closures*:

``` {.sourceCode .javascript}
function show_comment(parent, comment_id, content) {
    var comment_div = $('<div>').addClass('comment').text(content).appendTo(parent);
    var comment_like = $('<button>Like</button>').appendTo(comment_div);
    comment_like.click(function() {
        // Closure #1
        $.ajax('/me_too', {
            data: { comment_id: comment_id },
            success: function () {
                // Closure #2,
                comment_div.addClass("liked");
                comment_like.hide();
            }
        });
    });
}
```

`comment_id`, `comment_div` and `comment_like` are kept in the lexical
scope of the `show_comment` function, and so are still available when
the "Like" button is clicked ... the callback functions called by
`comment_like.click` and by `$.ajax` can use these variables. If you
call `show_comment` many times, each call will have its own lexical
scope with its own values to remember.

There is one major trap: *functions* create lexical scopes, not
*blocks*. So the following:

``` {.sourceCode .javascript}
function not_going_to_work() {
    for (var i=0; i<10; i++) {
    $('<button>').text("Button "+i).click(
            function () {
                alert("Button " + i + " Clicked");
            }
        ).appendTo(document.body);
    }
}
```

... isn't going to work. Whichever button you click, it'll say "Button
10 Clicked", because the loop counter `i` exists in only one scope, that
of the `not_going_to_work` function.

To get around this, we add an anonymous inner function so that each
button has its own associated scope:

``` {.sourceCode .javascript}
function is_going_to_work() {
    for (var i=0; i<10; i++) {
        (function (n) {
        $('<button>').text("Button "+n).click(
                function () {
                    alert("Button " + n + " Clicked");
                }
            ).appendTo(document.body);
        })(i);
    }
}
```

I've written a bunch of HTML5 / javascript stuff in recent years which
uses closures as a way of never actually having to traverse the DOM. It
is easy, fast, works well within the Chrome debugger and reduces your
reliance on jQuery (etc).
