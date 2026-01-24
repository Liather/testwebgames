const socket = io();

// trys to retrieve players ID and print it
let playerID = localStorage.getItem("playerID");

// if no playerID in localstorage - generate one
if (!playerID) {
    playerID = crypto.randomUUID();
    localStorage.setItem("playerID", playerID);
    console.log(localStorage.getItem("playerID"));
}

// button event listeners 
document.getElementById('createRoomButton').addEventListener('click', () => {
    socket.emit('createRoom_request', { 
      "playerID": playerID
    });
});

document.getElementById('submitRoomCodeButton').addEventListener('click', () => {
    var code = document.getElementById("roomCodeInput").value;
    socket.emit('joinRoom_request', { 
      "code": code
    });
});

// responses
socket.on('roomCreated', (data) => {
  window.location.href = `/room?code=${data.roomCode}`;
})

socket.on('roomFound', (data) => {
  window.location.href = `/room?code=${data.roomCode}`;
})

// error messages
socket.on('error', (data) => {
  alert(data);
})