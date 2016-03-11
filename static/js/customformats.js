/**
 * Created by nicolet on 15/01/16.
 */
window.onload = function () {
    var p_elements = document.getElementById('content').getElementsByTagName('p');
    var unixNewLine = new RegExp("\n", "g");
    for (var i = p_elements.length - 1; i >= 0; i--) {
        p_elements[i].innerHTML = p_elements[i].innerHTML.replace(unixNewLine, '<br/>');
    }
}