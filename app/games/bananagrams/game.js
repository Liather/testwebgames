const socket = io();

let playerID = localStorage.getItem("playerID");

// TODO - CHECK IF PLAYER ID IS PART OF THE ROOMS PLAYERS
if (!playerID) { // TODO - OR IF PLAYERID IS NOT PART OF PLAYERS IN ROOM
    // if no playerID (can only get on index.html) -> send back to index.html
    window.location.href = `/`;
    // Maybe send the player an alert saying no playerID was found
        // - Let's them know why they were sent back to the home page
}

let selectedTile = null;

const roomCode = new URLSearchParams(window.location.search).get('code');

socket.emit('joinedGame', {
    'roomCode': roomCode,
    'playerID': playerID
});

// Event listeners
document.getElementById('peelButton').addEventListener('click', () => {
    socket.emit('peelRequest', {
        "playerID": playerID,
        "roomCode": roomCode
    });
});

document.getElementById('upButton').addEventListener('click', () => {
    socket.emit('shiftTiles', {
        "playerID": playerID,
        "roomCode": roomCode,
        "direction": "up"
    });
});

document.getElementById('downButton').addEventListener('click', () => {
    socket.emit('shiftTiles', {
        "playerID": playerID,
        "roomCode": roomCode,
        "direction": "down"
    });
});

document.getElementById('leftButton').addEventListener('click', () => {
    socket.emit('shiftTiles', {
        "playerID": playerID,
        "roomCode": roomCode,
        "direction": "left"
    });
});

document.getElementById('rightButton').addEventListener('click', () => {
    socket.emit('shiftTiles', {
        "playerID": playerID,
        "roomCode": roomCode,
        "direction": "right"
    });
});

// error messages
socket.on('error', (data) => {
    alert(data.message);

    //send player back to index if no uuid
    if (data.message == "invalidPlayer") {
        window.location.href = `/`;
    }
})

// WHEN GAME DATA IS SENT TO THE PLAYER
socket.on('gameData', (data) => {
    console.log(data);
    selectedTile = null;

    // render tiletray ------------------------------------------------
    let tileTray = document.getElementById("tileTray");
    tileTray.innerHTML = " ";
    
    data.tileTray.forEach((tile, index) => {
        const tileDiv = document.createElement('div');
        tileDiv.className = 'tile';
        tileDiv.textContent = tile;
        selectedTile = tile;
    
        tileDiv.addEventListener('click', () => {
        selectedTile = {
            source: 'tray',
            tile: tile,
            trayIndex: index
        };
        console.log('Selected tray tile:', selectedTile);
    });

        tileTray.appendChild(tileDiv);
    });

    // render board ------------------------------------------------
    let board = document.getElementById("board");
    board.innerHTML = " ";

    data.board.forEach((row, y) => {
        row.forEach((cell, x) => {
            const cellDiv = document.createElement('div');
            cellDiv.className = 'cell';
            cellDiv.textContent = cell;

            if (cell !== '') {
                cellDiv.className = 'poo'
            }
            
            // SELECT TILE FROM TRAY
            cellDiv.addEventListener('click', () => {
                if (cell !== '') {
                    selectedTile = {
                        source: 'board',
                        tile: cell,
                        x: x,
                        y: y
                    };
                    console.log("Selected board tile", selectedTile);
                    return;
                }


                if (cell === '' && selectedTile) {

                    // PLACE TILE
                    if (selectedTile.source === 'tray') {
                        console.log("placetile")
                        socket.emit('placeTileRequest', {
                            roomCode,
                            playerID,
                            trayIndex: selectedTile.trayIndex,
                            x,
                            y
                        });
                    }

                    // MOVE TILE
                    if (selectedTile.source === 'board') {
                        console.log("moveTile")
                        socket.emit('moveTileRequest', {
                            roomCode,
                            playerID,
                            fromX: selectedTile.x,
                            fromY: selectedTile.y,
                            toX: x,
                            toY: y
                        });
                    }

                    selectedTile = null;
                }
            });

            board.appendChild(cellDiv);
        });
    });
})