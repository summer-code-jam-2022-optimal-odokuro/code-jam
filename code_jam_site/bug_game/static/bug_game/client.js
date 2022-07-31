let game = null;
let player = null;

const keymap = new Map([[87, "up"], [53, "down"], [41, "left"], [44, "right"], [32, "attack"]]);


const GRID = 16;
// This is the "pixel size" of each tile

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

function getRoom() {
    return exampleMap
}

room = getRoom()

function getRoomBuffer(room, players, enemies) {
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

webSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    //unpacking code: tbd
    let temp_room = data['room']
    let temp_players = data['players']
    let temp_enemies = data['enemies']

    let roomBuffer, roomBufferContext;
    [roomBuffer, roomBufferContext] = getRoomBuffer(temp_room, temp_players, temp_enemies)
    mapContext.drawImage(roomBuffer, 0, 0)
}

webSocket.onclose = function(e) {
    console.error("bruh");
}

window.addEventListener("keydown", function(event){
    if (event.defaultPrevented){
        return;
    }

    let handled = false;
    let input = 'None';

    // Apparently this is deprecated
    // Oh well
    if (event.keyCode !== undefined){
        handled = true;
        if (keymap.has(event.keyCode)){
            input = keymap.get(event.keyCode)
        }
    }

    if (handled) {
        let msg = {'input': input}

        webSocket.send(JSON.stringify(msg))
        event.preventDefault()
    }
}, true)
