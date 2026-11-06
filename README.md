# J.A.R.V.I.S Voice Assistant (ASCEND Project Showcase, Voice AI and Conversational Agents)

A voice assistant with a movie-style interface. It answers questions in English and Hindi, and it controls the laptop it runs on.

## The problem we solved
Voice assistants usually need an app, an account, and cannot control your own laptop. Jarvis runs on your laptop, answers any question with an AI model, and runs laptop commands only from a safe list.

## Features
- Answers general questions by voice or typing (English and Hindi)
- Opens apps (Notepad, Calculator, Paint, Chrome, Edge, Camera, Settings) and websites
- Searches Google and YouTube, controls volume
- **Asks Allow / Deny before shutdown, restart or lock**
- Works in any browser: if the browser blocks speech recognition, the server listens instead

## How it works
- `index.html`: interface, microphone, spoken replies (browser speech)
- `server.py`: Python server (no extra packages). It matches commands against a fixed allowlist, and sends all other questions to the Gemini API
- It listens only on `127.0.0.1` and rejects requests from other websites or other computers
- The API key is typed hidden and kept only in memory for that session. It is never saved in a file

## Install and run (Windows)
1. Install Python 3 from python.org (tick "Add Python to PATH").
2. Get a free API key at aistudio.google.com (Get API key).
3. Double-click `start.bat`, paste the key when asked (it stays hidden). The browser opens at http://127.0.0.1:8765
4. Tap the glowing core and speak, or type.

## Limits
- Windows only for laptop commands
- Free Gemini tier has daily limits, and Google may use free-tier chats to improve its products. Do not say private things
- It cannot read live news
- Needs internet

## Test scenarios
See `TEST-SCENARIOS.md`.

## Team contributions
- **Tanveer ahmed ** 
- **shaik mustayeen** 
