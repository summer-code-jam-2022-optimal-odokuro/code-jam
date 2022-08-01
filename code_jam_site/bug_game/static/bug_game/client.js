let game = null;
let player = null;

const keymap = new Map([[87, "up"], [53, "down"], [41, "left"], [44, "right"], [32, "attack"]])
const colormap = new Map([[0, "white"], [1, "darkslategray"], [2, "black"], [3, "lightgray"]])

/*server constants:
DOOR_CHAR = 3
WALL_CHAR = 2
ROCK_CHAR = 1
NONE_CHAR = 0*/

const GRID = 8;
// This is the "pixel size" of each tile

const gameId = JSON.parse(document.getElementById('game-id').textContent);

const webSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/ingame/'
    + gameId
    + '/'
);

function getRoomBuffer(room, players, enemies, map) {
    console.log("getting room buffer")

    const buffer = document.createElement('canvas');
    buffer.width = map.width
    buffer.height = map.height
    const bufferContext = map.getContext("2d");

    for (let [ridx, row] of room.entries()) {
        for (let [cidx, col] of row.entries()) {
            bufferContext.fillStyle = colormap[col]
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
    console.log("received message")

    const data = JSON.parse(e.data);
    //unpacking code: tbd
    let temp_room = data['room']
    let temp_players = data['players']
    let temp_enemies = data['enemies']

    console.log('room: ' + temp_room)
    console.log('players: ' +  temp_players)
    console.log('enemies' + temp_enemies)

    const map = document.getElementById("map");
    map.width = temp_room.length * GRID;
    map.height = temp_room[0].length * GRID;
    const mapContext = map.getContext("2d");

    let roomBuffer, roomBufferContext;
    [roomBuffer, roomBufferContext] = getRoomBuffer(temp_room, temp_players, temp_enemies, map)
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
