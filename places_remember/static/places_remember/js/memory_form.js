let latitude = document.getElementById("id_latitude");
let longitude = document.getElementById("id_longitude");
let zoom = document.getElementById("id_zoom");

ymaps.ready(function () {
    // Map creation
    let myMap = new ymaps.Map("map", {
        // Coordinates of the map center
        center: [Number.parseFloat(latitude.value), Number.parseFloat(longitude.value)],
        // Zoom level in a range from 0 (entire world) to 21
        zoom: Number.parseInt(zoom.value)
    });
    window.myMap = myMap;

    // Synchronize map and form inputs
    myMap.events.add('actionend', function () {
        let c = myMap.getCenter();
        latitude.value = c[0];
        longitude.value = c[1];
        zoom.value = myMap.getZoom();
        c = `Lat: ${latitude.value}, Lon: ${longitude.value}, Zoom: ${zoom.value}`;
        console.log(c);
    });
});
