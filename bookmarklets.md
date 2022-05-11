Useful Bookmarklets
===================

### Encode Bookmarklets
Paste JS code into [Bookmarklet Maker](https://caiorss.github.io/bookmarklet-maker/)

### Decode Bookmarklets
[Decode Javascript Bookmarklet - Stack Overflow](https://stackoverflow.com/questions/48042450/decode-javascript-bookmarklet):

> In browser JS console, run:
> ```javascript
> b = '...'  // Paste bookmarklet in single-quotes and escape internal single quotes
> console.log(decodeURIComponent(b.substring(11)));
> ```

Then copy and format the code and remove the wrapping `(function() {...})()`

CopyAnchor
----------
```javascript
/* Copied from https://gist.github.com/bradleybossard/3667ad5259045f839adc */
function copyToClipboard(text) {
    if (window.clipboardData && window.clipboardData.setData) {
        /*IE specific code path to prevent textarea being shown while dialog is visible.*/
        return clipboardData.setData("Text", text);
    } else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
        var textarea = document.createElement("textarea");
        textarea.textContent = text;
        textarea.style.position = "fixed";  /* Prevent scrolling to bottom of page in MS Edge.*/
        document.body.appendChild(textarea);
        textarea.select();
        try {
            return document.execCommand("copy");  /* Security exception may be thrown by some browsers.*/
        } catch (ex) {
            console.warn("Copy to clipboard failed.", ex);
            return false;
        } finally {
            document.body.removeChild(textarea);
        }
    }
}
var anchor = '⚓️ ' + document.title;
copyToClipboard(anchor);
```

CopyM⬇︎
------
```javascript
/* Copied from https://gist.github.com/bradleybossard/3667ad5259045f839adc */
function copyToClipboard(text) {
    if (window.clipboardData && window.clipboardData.setData) {
        /*IE specific code path to prevent textarea being shown while dialog is visible.*/
        return clipboardData.setData("Text", text);
    } else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
        var textarea = document.createElement("textarea");
        textarea.textContent = text;
        textarea.style.position = "fixed";  /* Prevent scrolling to bottom of page in MS Edge.*/
        document.body.appendChild(textarea);
        textarea.select();
        try {
            return document.execCommand("copy");  /* Security exception may be thrown by some browsers.*/
        } catch (ex) {
            console.warn("Copy to clipboard failed.", ex);
            return false;
        } finally {
            document.body.removeChild(textarea);
        }
    }
}
var markdown = '[' + document.title + '](' + window.location.href + ')';
copyToClipboard(markdown);
```

Copy rST
--------
```javascript
/* Copied from https://gist.github.com/bradleybossard/3667ad5259045f839adc */
function copyToClipboard(text) {
    if (window.clipboardData && window.clipboardData.setData) {
        /*IE specific code path to prevent textarea being shown while dialog is visible.*/
        return clipboardData.setData("Text", text); 
    } else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
        var textarea = document.createElement("textarea");
        textarea.textContent = text;
        textarea.style.position = "fixed";  /* Prevent scrolling to bottom of page in MS Edge.*/
        document.body.appendChild(textarea);
        textarea.select();
        try {
            return document.execCommand("copy");  /* Security exception may be thrown by some browsers.*/
        } catch (ex) {
            console.warn("Copy to clipboard failed.", ex);
            return false;
        } finally {
            document.body.removeChild(textarea);
        }
    }
}
var rstLink = '`' + document.title + ' <' + window.location.href + '>`__';
copyToClipboard(rstLink);
```



---
