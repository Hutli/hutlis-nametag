var input;
var output;
function onload() {
    input = document.getElementById('input');
    output = document.getElementById('output');
}
function set_name() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        output.innerHTML = "Setting...";
        if (xhr.readyState === 4) {
            output.innerHTML = xhr.response.replace(/\\r?\\n/g, '<br/>');
        }
    }
    xhr.open('get', '/api/nametag/' + input.value, true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    xhr.send();
}