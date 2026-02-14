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

socket.emit('joinedRoom', {
    'roomCode': roomCode,
    'playerID': playerID
});

// Event listeners
document.getElementById('setNicknameButton').addEventListener('click', () => {
    var newNickname = document.getElementById("nicknameInput").value;
    socket.emit('setNicknameRequest', { 
      "newNickname": newNickname,
        "playerID": playerID,
        "roomCode": roomCode
    });
    document.getElementById("nicknameInput").value = ""; // clear nickname input
});

document.getElementById('startGameButton').addEventListener('click', () => {
    socket.emit('startGameRequest', {
        "playerID": playerID,
        "roomCode": roomCode
    });
});

function dropdownOnSelect(value){
    socket.emit('setSelectedGame', {
        'selectedGame': value,
        'playerID': playerID,
        'roomCode': roomCode
    });
}

// socket on

// error messages
socket.on('error', (data) => {
    if (data.message == "invalidPlayer") {
        window.location.href = `/`;
    }
})

// playerList
    // show roles (highlight host)
    // add remove button for host
    // add ready status and button
    // add event listener for buttons
socket.on('playerData', (data) => {
    const players = data.players;
    
    playerDataElement = document.getElementById("playerData"); //ul
    playerDataElement.innerHTML = "";

    players.forEach(player => {
        const li = document.createElement("li");

        // needs to change the width of the li
        if(player.isHost) {
            li.style.backgroundColor = "#ffd700";
        }

        const nameSpan = document.createElement("span");
        nameSpan.textContent = player.playerNickname;
        li.appendChild(nameSpan);

        const roleSpan = document.createElement("span");
        roleSpan.textContent = ` (${player.playerRole})`;
        li.appendChild(roleSpan);

        // show host controls
        if(player.isHost && player.playerID == playerID) {
            console.log("Placeholder for host controls");
        }

        playerDataElement.appendChild(li);
        //console.log(player.isHost);
    });
})

socket.on('selectedGame', (data) => {
    console.log(data);
    const selectedGameElement = document.getElementById("selectedGame");
    selectedGameElement.textContent = `Selected Game: ${data.selectedGame}`;
});

// Show game data
socket.on('availableGames', (data) => {
    const gameSelectElement = document.getElementById("gameSelect");
    gameSelectElement.innerHTML = "";

    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Choose game";
    defaultOption.disabled = true;
    defaultOption.selected = true;
    gameSelectElement.appendChild(defaultOption);

    data.availableGames.forEach(game => {
        const option = document.createElement("option");
        option.value = game;
        option.textContent = game;
        gameSelectElement.appendChild(option);
    });
    console.log(data);

    // GAME CONFIG

});

// gameData
    // selectedGame
    // gameConfig
        // only allow host to change game config
            // Check playerID (ifHost) when game config change request made to ensure no inspect element shananagins
 
socket.on('startGame', (data) => {
    console.log("START THE GAME");
    console.log(data)
});