const socket = io();

let playerID = localStorage.getItem("playerID");

// TODO - CHECK IF PLAYER ID IS PART OF THE ROOMS PLAYERS
if (!playerID) { // TODO - OR IF PLAYERID IS NOT PART OF PLAYERS IN ROOM
    // if no playerID (can only get on index.html) -> send back to index.html
    window.location.href = `/`;
    // Maybe send the player an alert saying no playerID was found
        // - Let's them know why they were sent back to the home page
}

const roomCode = new URLSearchParams(window.location.search).get('code');
const roomCodeTitle = document.getElementById("title");
roomCodeTitle.textContent = `ROOM CODE: ${roomCode}`;

socket.emit('joinedGame', {
    'roomCode': roomCode,
    'playerID': playerID
});


