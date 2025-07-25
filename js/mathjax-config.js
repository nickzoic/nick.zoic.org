// THANKS https://www.stderr.nl/Blog/Blog/MathJaxInMarkdown.html
MathJax = {
  options: {
    // Remove <code> tags from the blacklist. Even though we pass an
    // explicit list of elements to process, this blacklist is still
    // applied.
    skipHtmlTags: { '[-]': ['code'] },
  },
  tex: {
    // By default, only \( is enabled for inline math, to prevent false
    // positives. Since we already only process code blocks that contain
    // exactly one math expression and nothing else, it is also fine to
    // use the nicer $...$ construct for inline math.
    inlineMath: { '[+]': [['$', '$']] },
  },
  startup: {
    // This is called on page ready and replaces the default MathJax
    // "typeset entire document" code.
    pageReady: function() {
      var codes = document.getElementsByTagName('code');
      var to_typeset = [];
      for (var i = 0; i < codes.length; i++) {
        var code = codes[i];
        // Only allow code elements that just contain text, no subelements
        if (code.childElementCount === 0) {
          var text = code.textContent.trim();
          inputs = MathJax.startup.getInputJax();
          // For each of the configured input processors, see if the
          // text contains a single math expression that encompasses the
          // entire text. If so, typeset it.
          for (var j = 0; j < inputs.length; j++) {
            // Only use string input processors (e.g. tex, as opposed to
            // node processors e.g. mml that are more tricky to use).
            if (inputs[j].processStrings) {
              matches = inputs[j].findMath([text]);
              if (matches.length == 1 && matches[0].start.n == 0 && matches[0].end.n == text.length) {
                // Trim off any trailing newline, which otherwise stays around, adding empty visual space below
                code.textContent = text;
                to_typeset.push(code);
                code.classList.add("math");
                if (code.parentNode.tagName == "PRE")
                  code.parentNode.classList.add("math");
                break;
              }
            }
          }
        }
      }
      // Code blocks to replace are collected and then typeset in one go, asynchronously in the background
      MathJax.typesetPromise(to_typeset);
    },
  },
};
