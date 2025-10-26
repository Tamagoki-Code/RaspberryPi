# 🕹️ Raspberry Pi Pico W Maze Game

A browser-based maze game hosted directly from the **Raspberry Pi Pico W**.  
Players use **physical buttons** to move through the maze, aiming to reach the goal in the shortest time possible while earning points.  
When the player reaches the finish point, a **“YOU WIN”** message is displayed with the **final score** and **time**.

---

## 🚀 Features

- Real-time player movement using GPIO buttons  
- Built-in Wi-Fi web server hosted by the Pico W  
- Displays **Score** and **Time** dynamically  
- “You Win” screen with live time and score stats  
- Runs entirely offline — no internet connection required  

---

## 🧰 Hardware Requirements

| Component | Description |
|------------|-------------|
| Raspberry Pi Pico W | Main microcontroller with Wi-Fi capability |
| 4 Push Buttons | For player controls (Up, Down, Left, Right) |
| Breadboard + Jumper Wires | For connecting buttons to the Pico |
| Power Supply | USB cable connected to computer or adapter |

---

## ⚙️ Software Requirements

| Software | Version / Info |
|-----------|----------------|
| **MicroPython** | Latest version for Pico W |
| **Thonny IDE** | For uploading and running `.py` files |
| **Web Browser** | To access the maze game (via Wi-Fi) |

---

## 💻 Setup and Installation

### 1. Flash MicroPython on Pico W
If not already installed, flash MicroPython onto your Pico W using the **Thonny IDE**.

1. Hold **BOOTSEL** while plugging in the Pico.
2. In Thonny: `Tools → Options → Interpreter → Install MicroPython`.
3. Select **Raspberry Pi Pico W**.

---

### 2. Upload Files
Copy the following files to your Pico W’s root directory:
- `main.py`
- `static/maze.html`
- `static/script.js`
- `static/style.css`

---

### 3. Connect Buttons
| Direction | GPIO Pin |
|------------|-----------|
| Left | GP0 |
| Right | GP1 |
| Up | GP2 |
| Down | GP3 |

Each button should connect between the GPIO pin and **GND**.

---

### 4. Run the Game
1. Run `main.py` in Thonny.  
2. On your device, connect to the Wi-Fi network created by the Pico (e.g., `PicoMazeGame`).  
3. Open your browser and go to **http://192.168.4.1**.  
4. Play the maze game using your physical buttons!

---

## 🧠 How It Works

1. **MicroPython Server** — The Pico W runs a lightweight web server that serves `maze.html` to browsers connected to its Wi-Fi access point.  
2. **Physical Controls** — Each button press triggers a corresponding movement event (up, down, left, right).  
3. **Maze Rendering** — The maze and player ball are drawn in the browser using `<canvas>` and JavaScript.  
4. **Win Condition** — When the player reaches the end point:
   - The game displays `YOU WIN!`
   - Shows the final **Score** and **Time**
   - Resets after a short delay or manual restart

---

## 📄 Documentation

### 🧩 main.py
- **Purpose:** Handles GPIO input, sets up the Pico W as a Wi-Fi AP, and serves web pages.  
- **Key Sections:**
  - **Button Initialization:**  
    ```python
    button_left = Pin(0, Pin.IN, Pin.PULL_DOWN)
    button_right = Pin(1, Pin.IN, Pin.PULL_DOWN)
    button_up = Pin(2, Pin.IN, Pin.PULL_DOWN)
    button_down = Pin(3, Pin.IN, Pin.PULL_DOWN)
    ```
  - **Wi-Fi Access Point Setup:**  
    ```python
    ap = network.WLAN(network.AP_IF)
    ap.config(essid='PicoMazeGame')
    ap.active(True)
    ```
  - **Web Server Setup:** Uses sockets to serve HTML and handle button actions.

---

### 🎨 maze.html / script.js
- **Purpose:** Front-end interface for rendering the maze, handling player movement, and tracking time and score.
- **Main Functions:**
  - `movePlayer(direction)` – Moves the ball inside the maze.
  - `checkCollision()` – Detects wall boundaries.
  - `checkWin()` – Displays “YOU WIN!” screen with final score and time.
- **Game HUD:**
  ```html
  <div id="hud">
    Score: <span id="score">0</span> | Time: <span id="timer">0s</span>
  </div>
🎨 style.css
Defines maze layout, colors, and text styling.

Uses bright color contrast for readability.

Styles win message with large centered yellow text.

🧮 Score and Timer Logic
The timer starts automatically when the maze loads.

The score can increase based on actions (optional to modify in JS).

On win, both score and time are displayed clearly in the victory message.

🛠️ Future Improvements
Add multiple maze levels

Implement scoring system based on completion time

Save best scores to local storage

Add sound or background music

🏆 Author
Developed by: CS 121 Group
Language: MicroPython + HTML/JS
Repository: (https://github.com/Tamagoki-Code/RaspberryPi)

📜 License
This project is licensed under the MIT License — you’re free to use, modify, and share it with attribution.
