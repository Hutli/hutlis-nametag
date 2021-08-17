var input;
var output;
function onload() {
    input = document.getElementById('input');
    output = document.getElementById('output');
}
function set_name() {
    var xhr = new XMLHttpRequest();
    output.disabled = true;
    var orig_value = output.value;
    output.value = "Setting...";
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            output.disabled = false;
            output.value = orig_value;
        }
    }
    xhr.open('get', '/api/nametag/' + encodeURIComponent(input.value), true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    xhr.send();
}