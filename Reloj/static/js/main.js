var selectElement = document.getElementById('select');

var optionValue = selectElement.value;


var socket = new WebSocket('ws://127.0.0.1:8000/ws/myconsumer/' + optionValue + '/');



const storedSelection = localStorage.getItem('selectedOption');
if (storedSelection) {
    selectElement.value = storedSelection; 
}

selectElement.addEventListener('change', function() {
    const optionValue = selectElement.value;
    socket.send(JSON.stringify({
        'option': optionValue,
    }));


    // Almacena la selección en el almacenamiento local
    localStorage.setItem('selectedOption', optionValue);
});

function sendMsj() {
    console.log('MENSAJE enviandose' + optionValue);

    socket.send(JSON.stringify({'option': optionValue}));
}

socket.onopen = function(e) {
    // Conexión abierta, enviar el valor seleccionado
    var optionValue = selectElement.value;
    socket.send(JSON.stringify({
        'option': optionValue,
    }));

    console.log('Ws abierto')

    if (socket.readyState === WebSocket.OPEN) {
        setInterval(() => {
            sendMsj()
        }, 1000);
    } 

};

socket.onmessage = function(data) {

    var data = JSON.parse(data.data);
    var option = data.message;
    var hr = data.hr;
    var sc = data.sc;
    var mn = data.mn;

    clock = document.getElementById('clock');

    clock.innerHTML = `<span id="hr">${hr}</span> : <span id="mn">${mn}</span> : <span id="sc">${sc}</span>`
};

socket.onclose = function(e) {
    // Conexión cerrada
    console.log('Ws cerrado')
};