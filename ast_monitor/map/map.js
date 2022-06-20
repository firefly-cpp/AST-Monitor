function initializeMap() {
    const map = L.map('map').setView([46.55470, 15.64590], 16);

    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18
    }).addTo(map);

    L.marker(map.getCenter()).addTo(map);
}