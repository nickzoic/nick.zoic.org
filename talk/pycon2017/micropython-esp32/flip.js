(function () {
    var p = 0; 

    function change_slide(n) {
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
    
    window.onkeydown = function (e) {
        var k = e.keyCode;
        if (k == 27) change_slide(0);
        else if (k == 48) change_slide(10);
        else if (k >= 49 && k <= 57) change_slide(k - 48);
        else if (k == 39 || k == 32 || k ==  34) change_slide(p+1);
        else if (k == 37 || k == 8 || k == 33 ) change_slide(p-1);
        else return;

        e.preventDefault();
        document.location.hash = p || '';
    }
})();
