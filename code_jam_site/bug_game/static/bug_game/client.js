let game = null;
let player = null;

const GRID = 10;
// This is the "pixel size" of each tile

const game_map = JSON.parse(document.getElementById('game_map').textContent);

const map = document.getElementById("map");
map.width = 80 * GRID;
map.height = 80 * GRID;
const mapContext = map.getContext("2d");

const gameId = JSON.parse(document.getElementById('game-id').textContent);

const webSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/ingame/'
    + gameId
    + '/'
);

webSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    //unpacking code: tbd

}

webSocket.onclose = function(e) {
    console.error("bruh");
}

function getRoom() {
    return exampleMap
}

room = getRoom()

function getRoomBuffer(room) {
    const buffer = document.createElement('canvas');
    buffer.width = room.length * GRID;
    buffer.height = room[0].length * GRID;
    const bufferContext = map.getContext("2d");

    for (let [ridx, row] of room.entries()) {
        for (let [cidx, col] of row.entries()) {
            if (col) {
                if (cidx === 0 || ridx === 0 || cidx === 79 || ridx === 79) {
                    bufferContext.fillStyle = "black"
                } else {
                    bufferContext.fillStyle = "grey"
                }

            } else {
                bufferContext.fillStyle = "white"
            }
            // here is where we would paste the game entity over

            bufferContext.fillRect(ridx * GRID, cidx * GRID, GRID, GRID)
        }
    }

    return [buffer, bufferContext];
}

// draw a one grid-unit wide and tall triangle
function drawTriangle(x, y, context) {
    context.beginPath();
    context.fillStyle = 'green';
    context.moveTo(x * GRID, y * GRID + GRID);
    context.lineTo(x * GRID + GRID / 2, y * GRID);
    context.lineTo(x * GRID + GRID, y * GRID + GRID);
    context.fill();
}

let roomBuffer, roomBufferContext;
[roomBuffer, roomBufferContext] = getRoomBuffer(room)

mapContext.drawImage(roomBuffer, 0, 0)
