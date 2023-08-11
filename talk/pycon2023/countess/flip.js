(function () {
    var p = 0; 

    function change_slide(n) {
	window.scrollTo(0,0);
        var s = document.getElementsByClassName('slide');
        if (n<0) n = s.length;
        if (!n || n < 0 || n > s.length) n = 0;
        if (p==n) return;
        if (p) s[p-1].className="slide";
        if (n) s[n-1].className="slide show";
        if (n && !p) {
            document.body.className="flip-hide";
            setTimeout(function() { document.body.className = "flip"; }, 1000);
        }
        if (p && !n) {
            document.body.className = "flip-unhide";
            setTimeout(function () { document.body.className = ""; }, 1000);
        }
        p = n; 
    }

    var n = parseInt(document.location.hash.substring(1));
    if (n) window.onload = function () { change_slide(n); }
   

    // my laser presenter thingy has a "<" PgUp key,
    //  a ">" PgDn key, 🖵 -with-⏵︎ which sends 
    // alternating F5 and Escape keys (why‽), and 🖵  
    // which sends ".".  Can't catch F5 so I'm using
    // "." to start the slideshow and "Esc" to exit it.
	
    window.onkeydown = function (e) {
        var k = e.keyCode;

	// escape exits the slideshow
        if (k == 27) change_slide(0);

	// period "." key enters the slideshow
	else if (k == 190) change_slide(1);

	// rightarrow, spacebar, page down
        else if (p > 0 && (k == 39 || k == 32 || k ==  34)) change_slide(p+1);

	// leftarrow, backspace, page up
        else if (p > 0 && (k == 37 || k == 8 || k == 33 )) change_slide(p-1);


        else return;

        e.preventDefault();
        document.location.hash = p || '';
    }
})();
