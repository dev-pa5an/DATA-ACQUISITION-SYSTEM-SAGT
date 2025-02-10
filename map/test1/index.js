// Initialize the map
var map = L.map('map').setView([51.49532, -0.07], 16); // Set the center coordinates and zoom level

// Define the bounds for your custom image
var imageUrl = 'map.jpg'; // Path to your custom image (replace with the correct path)
var imageBounds = [[51.49, -0.08], [51.5, -0.06]]; // Define the geographical bounds (top-left and bottom-right corners)

// Add the image as an overlay on the map
L.imageOverlay(imageUrl, imageBounds).addTo(map);

// // Optionally, you can add controls, markers, etc. on top of the image map if needed

// const map = L.map("map").setView([51.505, -0.09], 13);
// L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

const socket = io("http://localhost:3000");

let markers = {}; // Store marker references

// Load existing markers when connected
socket.on("load_markers", (serverMarkers) => {
    serverMarkers.forEach((marker) => addMarker(marker, false));
});

// Handle marker updates
socket.on("update_markers", (serverMarkers) => {
    clearMarkers();
    serverMarkers.forEach((marker) => addMarker(marker, false));
});

// Add marker function
function addMarker(markerData, emit = true) {
    const marker = L.marker([markerData.lat, markerData.lng], { draggable: true }).addTo(map);

    marker.on("dragend", function () {
        const { lat, lng } = marker.getLatLng();
        socket.emit("update_marker", { id: markerData.id, lat, lng });
    });

    markers[markerData.id] = marker;

    if (emit) {
        socket.emit("add_marker", markerData);
    }
}

// Remove all markers
function clearMarkers() {
    Object.values(markers).forEach(marker => map.removeLayer(marker));
    markers = {};
}

// Click to add new marker
map.on("click", (e) => {
    const markerData = {
        id: Date.now().toString(),
        lat: e.latlng.lat,
        lng: e.latlng.lng,
    };
    addMarker(markerData, true);
});