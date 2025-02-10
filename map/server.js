const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const cors = require("cors");

const app = express();
const server = http.createServer(app);

const io = new Server(server, {
  cors: {
    origin: "*", // Allow connections from any origin (adjust for security)
  },
});
const WebSocket = require("ws");

const wss = new WebSocket.Server({ port: 3000 });

let dataStore = [];
let markers = [];

wss.on("connectwsn", (ws) => {
    console.log("A user connected:", ws.id);

    // Send existing data to newly connected clients
    ws.emit("load_markers", markers);
    ws.send(JSON.stringify({ type: "initialize", data: dataStore }));
    // Listen for new marker events
    // ws.on("add_marker", (marker) => {
    //     markers.push(marker); // Store marker
    //     wss.emit("update_markers", markers); // Broadcast to all clients
    // });

    // // Listen for marker updates (e.g., movement)
    // ws.on("update_marker", (updatedMarker) => {
    //     markers = markers.map((m) => (m.id === updatedMarker.id ? updatedMarker : m));
    //     wss.emit("update_markers", markers);
    // });

    // // Listen for marker removal
    // ws.on("remove_marker", (markerId) => {
    //     markers = markers.filter((m) => m.id !== markerId);
    //     wss.emit("update_markers", markers);
    // });

    ws.on("message", (message) => {
        const receivedData = JSON.parse(message);

        if (receivedData.type === "newEntry") {
            dataStore.push(receivedData.data);

            // Broadcast the new entry to all clients
            wss.clients.forEach(client => {
                if (client.readyState === WebSocket.OPEN) {
                    client.send(JSON.stringify({ type: "newEntry", data: receivedData.data }));
                }
            });
        }
    });

    ws.on("close", () => console.log("Client disconnected"));
});

console.log("WebSocket server running on port 3000");
