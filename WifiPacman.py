from machine import Pin
import network
import socket
import time
import ure

# --------------------
# Buttons
# --------------------
button_left = Pin(0, Pin.IN, Pin.PULL_DOWN)
button_right = Pin(1, Pin.IN, Pin.PULL_DOWN)
button_up = Pin(2, Pin.IN, Pin.PULL_DOWN)
button_down = Pin(3, Pin.IN, Pin.PULL_DOWN)

# --------------------
# Pico W Wi-Fi AP
# --------------------
ssid = "PacmanPico"
password = "12345678"

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)
print("AP started, connect to:", ssid)

# --------------------
# HTML + JS
# --------------------
html = """<!DOCTYPE html>
<html>
<head>
<title>Pac-Man MicroPython</title>
<style>
html,body {margin:0;padding:0;overflow:hidden;background:black;color:white;font-family:sans-serif;}
canvas {display:block;}
#info {position:absolute;top:5px;left:5px;font-size:18px;}
#winner {
    position:absolute;
    top:50%;
    left:50%;
    transform:translate(-50%,-50%);
    font-size:48px;
    color:yellow;
    text-align:center;
    display:none;
}
</style>
</head>
<body>
<div id="info">Score: 0 | Time: 0s</div>
<div id="winner"></div>
<canvas id="game"></canvas>
<script>
let canvas = document.getElementById('game');
let ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let cell = 30;
let cols = Math.floor(canvas.width / cell);
let rows = Math.floor(canvas.height / cell);

let pac = {x:1, y:1};
let pellets = [];
let score = 0;
let startTime = Date.now();
let gameWon = false;

// --------------------
// Maze generation (recursive backtracking)
// --------------------
function generateMaze(w,h) {
    let maze = Array(h).fill().map(()=>Array(w).fill(1));
    function carve(x,y){
        let dirs=[[1,0],[-1,0],[0,1],[0,-1]];
        dirs.sort(()=>Math.random()-0.5);
        maze[y][x]=0;
        for(let [dx,dy] of dirs){
            let nx=x+dx*2, ny=y+dy*2;
            if(nx>0&&ny>0&&nx<w-1&&ny<h-1&&maze[ny][nx]==1){
                maze[y+dy][x+dx]=0;
                carve(nx,ny);
            }
        }
    }
    carve(1,1);
    return maze;
}

let grid = generateMaze(cols, rows);

// Create pellets (skip Pac-Man’s starting cell)
for(let r=0;r<rows;r++){
    for(let c=0;c<cols;c++){
        if(grid[r][c]==0 && !(c==pac.x && r==pac.y)) {
            pellets.push({x:c, y:r});
        }
    }
}

function draw(){
    ctx.fillStyle='black';
    ctx.fillRect(0,0,canvas.width,canvas.height);

    // Walls
    ctx.fillStyle='blue';
    for(let r=0;r<rows;r++){
        for(let c=0;c<cols;c++){
            if(grid[r][c]==1) ctx.fillRect(c*cell,r*cell,cell,cell);
        }
    }

    // Pellets
    ctx.fillStyle='white';
    for(let p of pellets){
        ctx.beginPath();
        ctx.arc(p.x*cell+cell/2,p.y*cell+cell/2,cell/6,0,2*Math.PI);
        ctx.fill();
    }

    // Pac-Man
    ctx.fillStyle='yellow';
    ctx.beginPath();
    ctx.arc(pac.x*cell+cell/2,pac.y*cell+cell/2,cell/2,0,2*Math.PI);
    ctx.fill();

    // Info
    let elapsed = Math.floor((Date.now()-startTime)/1000);
    document.getElementById('info').innerHTML = "Score: "+score+" | Time: "+elapsed+"s";
}

function canMove(nx,ny){
    if(nx<0||nx>=cols||ny<0||ny>=rows) return false;
    return grid[ny][nx]==0;
}

function updatePac(dir){
    if(gameWon) return;
    let nx=pac.x, ny=pac.y;
    if(dir=='LEFT') nx--;
    else if(dir=='RIGHT') nx++;
    else if(dir=='UP') ny--;
    else if(dir=='DOWN') ny++;
    if(canMove(nx,ny)){
        pac.x=nx; pac.y=ny;

        // Check if pellet eaten
        let before = pellets.length;
        pellets = pellets.filter(p=>!(p.x==pac.x && p.y==pac.y));
        let after = pellets.length;
        if(after < before) score++; // increment when pellet is eaten

        // Win condition
        if(pellets.length === 0){
            gameWon = true;
            let elapsed = Math.floor((Date.now()-startTime)/1000);
            document.getElementById('winner').innerHTML = 
                "YOU WIN!<br>Score: "+score+" | Time: "+elapsed+"s";
            document.getElementById('winner').style.display = "block";
        }
    }
}

draw();

setInterval(async ()=>{
    if(gameWon) return; // stop polling when game is done
    let r = await fetch('/buttons');
    let dir = await r.text();
    if(dir) updatePac(dir);
    draw();
}, 100);
</script>
</body>
</html>
"""

# --------------------
# Socket server
# --------------------
try:
    s.close()
except:
    pass

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
print('Listening on', addr)

while True:
    cl, addr = s.accept()
    req = cl.recv(1024)
    req = str(req)

    if "GET /buttons" in req:
        if button_left.value(): d="LEFT"
        elif button_right.value(): d="RIGHT"
        elif button_up.value(): d="UP"
        elif button_down.value(): d="DOWN"
        else: d=""
        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n")
        cl.send(d)
    else:
        cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n")
        cl.send(html)
    cl.close()
