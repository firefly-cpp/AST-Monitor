let map;

function initialize(){
    map = L.map('map').setView([46.55470, 15.64590], 16);

    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18
    }).addTo(map);

    const marker = L.marker(map.getCenter()).addTo(map);

    new QWebChannel(qt.webChannelTransport, (channel) => {
        window.MainWindow = channel.objects.MainWindow;
        if (typeof MainWindow != 'undefined') {
            // var onMapMove = function() { MainWindow.onMapMove(map.getCenter().lat, map.getCenter().lng) };
            // map.on('move', onMapMove);
            // onMapMove();
        }
    });
}