# 🟡 Pac-Man MicroPython (Raspberry Pi Pico W)

A browser-based Pac-Man game hosted directly from a **Raspberry Pi Pico W** running **MicroPython**.  
The Pico acts as a Wi-Fi Access Point and serves a simple HTML5 + JavaScript game page that can be controlled using **four physical buttons** connected to its GPIO pins.

---

## 🧩 Features

- 🕹️ **Real physical button control** (Up, Down, Left, Right)
- 📡 **Wi-Fi Access Point** mode (no router required)
- 🧱 **Procedurally generated maze** using recursive backtracking
- 🍒 **Pellet collection and scoring system**
- 🏁 **Win condition** when all pellets are collected
- 🕒 **Timer and score tracking**
- ⚡ **Runs entirely on the Pico W — no external server needed**

---

## ⚙️ Hardware Setup

| Component       | GPIO Pin | Description       |
|-----------------|-----------|-------------------|
| Left Button     | GP0       | Move Pac-Man left |
| Right Button    | GP1       | Move Pac-Man right |
| Up Button       | GP2       | Move Pac-Man up   |
| Down Button     | GP3       | Move Pac-Man down |

> ⚠️ All buttons use **PULL_DOWN** configuration.  
> Make sure to connect each button to **3.3V** on press.

---

## 🌐 How It Works

1. The Pico W starts in **Access Point (AP)** mode using:
   ```python
   ssid = "PacmanPico"
   password = "12345678"
Connect your phone or laptop to this Wi-Fi network.

Open a browser and visit http://192.168.4.1

The game loads directly from the Pico’s internal web server.

Pac-Man’s movement is controlled via GPIO button inputs.

The browser polls the Pico (/buttons) every 100ms to check for button states.

🧠 Code Structure
MicroPython Section
Sets up button input pins

Configures the Pico W as an AP

Hosts a socket-based HTTP server

Serves:

/ → HTML + JavaScript Pac-Man game

/buttons → Current button direction as plain text

JavaScript Game Section
Generates a random maze layout

Spawns pellets (excluding Pac-Man’s start position)

Handles drawing, movement, collision, and scoring

Ends the game with a “YOU WIN!” message showing final score and elapsed time

🕹️ Controls
Button	Action
⬅️ Left Button	Move left
➡️ Right Button	Move right
⬆️ Up Button	Move up
⬇️ Down Button	Move down

🏆 Win Condition
When all pellets are collected:

The game freezes

A centered message appears:

yaml
Copy code
YOU WIN!
Score: X | Time: Ys
🧾 Example Output (Serial Console)
vbnet
Copy code
AP started, connect to: PacmanPico
Listening on ('0.0.0.0', 80)
📂 File Overview
File	Description
main.py	Full MicroPython code (Pico W game host + button input)
README.md	This documentation file

🧰 Requirements
Raspberry Pi Pico W

MicroPython firmware (latest stable build)

Thonny IDE or any serial REPL

4x push buttons + jumper wires

🚀 Setup & Run
Flash your Pico W with MicroPython firmware.

Open Thonny and upload main.py.

Run the script — wait for:

arduino
Copy code
AP started, connect to: PacmanPico
On your phone/PC, connect to the PacmanPico Wi-Fi network.

Open http://192.168.4.1 in your browser.

Start playing Pac-Man!

🧑‍💻 Author
CS 121
Raspberry Pi Pico W Project • 2025

📜 License
This project is released under the MIT License.
You are free to modify, distribute, and use it for educational or personal projects.

⭐ If you enjoyed this project, consider giving it a star on GitHub!
