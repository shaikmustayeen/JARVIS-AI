# JARVIS AI Personal Assistant

**Theme:** Voice AI & Conversational Agents  
**Team Name:** Domain Expansion  
**Team Members:**  
- **Shaik Mustayeen** — Roll No: `25R11A6751`  
- **Tanveer Ahmed** — Roll No: `25R11A6740`  

---

## 📌 Project Overview

**JARVIS AI Personal Assistant** is an intelligent, low-latency, voice-driven assistant built with an Iron Man-inspired cinematic HUD interface. Unlike cloud-only assistants that require dedicated hardware or third-party accounts, JARVIS runs locally on the user's laptop, communicates through voice and text, and securely bridges modern Large Language Models (LLMs) with native Windows desktop and browser controls.

The assistant combines a zero-dependency Python backend with a high-performance web interface, Google's Gemini models, and a Manifest V3 browser extension to deliver natural conversational answers, real-time news briefings, foreground application launching, and browser tab lifecycle management.

---

## ✨ Key Features

- **🗣️ Natural Voice Interaction & Instant Speech:**
  - Full two-way voice communication with speech-to-text input and natural text-to-speech output using the browser's speech synthesis engine.
  - Asynchronous command execution ensures spoken replies begin immediately with zero delay.

- **💻 Native Windows Application Control:**
  - Dynamic discovery of installed applications by scanning Start Menu shortcuts (`.lnk` files in `%ProgramData%` and `%AppData%`).
  - Launches apps directly in the **active foreground** using native Windows ShellExecute (`os.startfile`) for apps like Notepad, Windows Camera, Calculator, WhatsApp, VS Code, Discord, Steam, MS Office, etc.
  - Safe, allowlist-based process termination (`taskkill`) by process name without constructing shell commands from user text.

- **🌐 Smart Browser Tab Management:**
  - Manifest V3 browser extension (`extension/`) specifically engineered for Brave and Chrome.
  - Secure communication between the extension and backend using an authorization pairing token.
  - Directly opens websites, tracks tab IDs, and enables voice commands like *"close it"*, *"close the youtube"*, or *"close tabs"* to close tabs cleanly.

- **📰 Live Categorized News & Real-Time Utilities:**
  - Real-time Google News RSS integration supporting targeted topics: **World News**, **India News**, **Technology**, and **Sports**.
  - Summarizes fresh headlines into concise 2-sentence voice briefings.
  - Real-time internet download speed testing powered by Cloudflare edge endpoints.
  - Instant offline answers for current time, date, greetings, and system status without contacting external APIs.

- **🛡️ Built-in Safety & Security Guardrails:**
  - Binds strictly to loopback (`127.0.0.1:8765`) and enforces strict `Host` and `Origin` validation.
  - **Explicit Allow / Deny confirmation cards** required in the interface before executing sensitive actions: laptop shutdown, restart, system lock, or closing all browser windows.
  - Secure API key handling: keys are prompted via secure password input in PowerShell (`start.ps1`), held only in volatile process memory for that session, and never written to disk.

- **⚡ High Performance & 0% Idle CPU:**
  - Pure CSS hardware-accelerated glowing Arc Reactor design replacing heavy SVG filter recalculations.
  - Waveforms and animations halt automatically when idle or when the tab is hidden, keeping idle CPU usage at **0.0%**.

---

## 🛠️ Technologies Used

| Layer | Technologies & Tools |
|---|---|
| **Frontend UI** | HTML5, CSS3 (Hardware-accelerated animations, responsive HUD grid), Vanilla JavaScript (ES6+) |
| **Voice & Audio** | Web Speech API (`SpeechRecognition`, `SpeechSynthesisUtterance`), Web Audio API (`AudioContext`, `MediaStreamAudioSourceNode`) |
| **Backend Server** | Python 3 (100% Standard Library: `http.server.ThreadingHTTPServer`, `urllib.request`, `subprocess`, `threading`, `json`, `pathlib`, `xml.etree.ElementTree`) |
| **AI / LLM Engine** | Google Gemini API (`gemini-2.0-flash`, `gemini-1.5-flash`, `gemini-2.5-flash`) via OpenAI-compatible endpoints |
| **Browser Extension** | Manifest V3, Service Workers (`background.js`), Chrome Tabs API, Chrome Storage API |
| **Operating System** | Windows 11 / Windows 10 Shell APIs, PowerShell COM scripting (`WScript.Shell`) |

---

## 📂 Project Structure

```text
jarvis-assistant/
│
├── server.py              # Local HTTP server, command parser, app discovery & LLM bridge
├── index.html             # Movie-style cybernetic Jarvis web HUD interface
├── start.bat              # One-click Windows batch launcher
├── start.ps1              # Secure hidden API key prompt & environment setup script
├── README.md              # Project documentation & team information
├── TEST-SCENARIOS.md      # Acceptance tests & verification test cases
│
└── extension/             # Manifest V3 browser extension for tab management
    ├── manifest.json      # Extension metadata & permissions
    ├── background.js      # Service worker polling server & controlling tabs
    ├── popup.html         # Extension status popup interface
    └── popup.js           # Extension popup script & pairing token management
```

---

## 🚀 Installation & Execution Instructions

### Prerequisites
1. **Operating System:** Windows 10 or Windows 11.
2. **Python:** Python 3.10 or higher installed from [python.org](https://www.python.org/) (ensure *"Add Python to PATH"* is checked during installation).
3. **Browser:** [Brave Browser](https://brave.com/) or Google Chrome.
4. **Gemini API Key:** A free API key from [Google AI Studio](https://aistudio.google.com/).

---

### Step 1: Install the Browser Extension (One-Time Setup)

To allow Jarvis to open and close browser tabs smoothly:
1. Open your browser and navigate to:
   - For Brave: `brave://extensions`
   - For Chrome: `chrome://extensions`
2. Toggle **Developer mode** on (switch located in the top-right corner).
3. Click the **Load unpacked** button (top-left corner).
4. Select the `extension` folder located inside this project directory (`jarvis-assistant/extension`).
5. The extension will automatically load and pair with Jarvis at `http://127.0.0.1:8765`.

---

### Step 2: Launch JARVIS

1. Double-click [`start.bat`](file:///C:/Users/ADMIN/Downloads/jarvis-assistant/start.bat).
2. When prompted:
   ```text
   Paste your Gemini API key (it stays hidden):
   ```
   Paste your Gemini key and press **Enter** (the input is masked for security).
3. The server starts immediately on `http://127.0.0.1:8765`, and your default browser opens the interface automatically.

---

### Step 3: Using Jarvis

Click the glowing core to start voice recognition, or type directly into the command input at the bottom:

| Category | Example Commands | Action Performed |
|---|---|---|
| **General AI** | *"What is the capital of France"*, *"Explain AI in simple words"* | Concise spoken answers powered by Gemini |
| **Websites** | *"Open YouTube"*, *"Open Gmail"*, *"Open GitHub"* | Opens the target website |
| **Tab Control** | *"Close it"*, *"Close YouTube"*, *"Close the YouTube"*, *"Close tabs"* | Closes the opened browser tabs |
| **Apps** | *"Open camera"*, *"Open notepad"*, *"Open WhatsApp"* | Launches application in the active foreground |
| **App Closing** | *"Close notepad"*, *"Close camera"*, *"Close WhatsApp"* | Safely closes application process |
| **Live News** | *"World news"*, *"Latest news"*, *"Tech news"*, *"India news"* | Fetches live Google News RSS and speaks summary |
| **System Info** | *"What time is it"*, *"What is today's date"*, *"How fast is my internet"* | Instant clock/date and live speed test |
| **Volume** | *"Volume up"*, *"Volume down"*, *"Mute"* | Adjusts Windows master volume |
| **Safety Actions**| *"Lock the laptop"*, *"Shut down"* | Displays Allow / Deny card before proceeding |

---

## 🧪 Verification & Acceptance Tests

All verification tests are documented with test cases in [`TEST-SCENARIOS.md`](file:///C:/Users/ADMIN/Downloads/jarvis-assistant/TEST-SCENARIOS.md).

---

## 👥 Team Information

**Team Name:** Domain Expansion  
**Theme:** Voice AI & Conversational Agents  

- **Shaik Mustayeen** — Roll No: `25R11A6751`
- **Tanveer Ahmed** — Roll No: `25R11A6740`
