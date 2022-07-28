let game = null;
let player = null;

const GRID = 10;

const map = document.getElementById("map");
map.width = 800;
map.height = 800;
const mapContext = map.getContext("2d");

function getRoom() {
    return exampleMap
}

const game_room = JSON.parse(document.getElementById("game_map").textContent)[0];
room = game_room();

function getRoomBuffer(room) {
    const buffer = document.createElement('canvas');
    buffer.width = 800;
    buffer.height = 800;
    const bufferContext = map.getContext("2d");

    for (let [ridx, row] of room.entries()) {
        for (let [cidx, col] of row.entries()) {
            if (col) {
                if (cidx == 0 || ridx == 0 || cidx == 79 || ridx == 79) {
                    bufferContext.fillStyle = "black"
                } else {
                    bufferContext.fillStyle = "grey"
                }

            } else {
                bufferContext.fillStyle = "white"
            }
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
