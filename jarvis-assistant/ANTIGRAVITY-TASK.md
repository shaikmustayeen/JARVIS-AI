# Task for the coding agent: finish and verify the Jarvis voice assistant

## Context
- Student project for a college showcase (theme: Voice AI and Conversational Agents). Deadline is very close, so work in the priority order below.
- Windows 11, Python 3.13, Brave browser, no admin rights. The user is not technical: keep it one-click (`start.bat`), prefer the Python standard library, add no heavy installs.
- Files in this folder: `server.py` (local Python server, port 8765), `index.html` (movie-style Jarvis interface), `start.bat` + `start.ps1` (ask for the Gemini API key hidden, set it as an environment variable for that session only, start the server), `README.md`, `TEST-SCENARIOS.md`.
- Read all the files first. The server talks to the Gemini API through its OpenAI-compatible endpoint (model `gemini-flash-lite-latest`; `gemini-flash-latest` was too slow). It also listens to the microphone by receiving WAV audio at `/api/listen`, because Brave blocks the browser speech API.
- The API key comes only from the environment variable `GEMINI_API_KEY`. Never write a key into any file. If you need it to test, ask the user to start `start.bat`.

## What the user wants (fix in this order)
1. **Speak Hindi and English.** Hindi speech in gives Hindi speech out, with the conversation text on screen in English. English in gives English out. It currently speaks only English. Find out why (for example, no Hindi voice installed in Windows, a wrong language tag, or the reply format) and fix it. The browser's `speechSynthesis` needs a Windows Hindi voice. If that is the cause, add a fallback that works without one, such as server-side text to speech through a Gemini TTS model. Check which TTS models this key can use by calling the models list endpoint. Make it work in Brave.
2. **Remove the lag.** The interface is heavy. I already removed blur and drop-shadow filters. Profile it and cut the rest (SVG animation cost, 40 waveform bars updated every frame, the scan line). Pause animations when the tab is hidden or idle. Idle CPU use should be very low.
3. **Close the tabs Jarvis opens.** Python cannot close a single browser tab, so `Ctrl+W` is only a weak workaround. Build a tiny Manifest V3 extension in `extension/` that Brave can load unpacked. It talks only to `http://127.0.0.1:8765`. Server commands: open URLs (remember the tab ids), close the tabs Jarvis opened ("close it"), close a tab by name, and list tabs. Add a simple pairing token so other programs and websites cannot control the browser. Add a short README section: how to load it (brave://extensions, Developer mode, Load unpacked).
4. **Control apps on the laptop.** Today there is a fixed list of apps. Add discovery of installed apps from the Start Menu shortcuts (`.lnk` files in `%ProgramData%\Microsoft\Windows\Start Menu\Programs` and `%AppData%\Microsoft\Windows\Start Menu\Programs`), so "open WhatsApp" or "open <any installed app>" works. Support "close <app>" by process name. Keep everything allowlist-based, with no shell command ever built from user text.
5. **Live news.** Google News RSS is already wired in. Verify it. Improve: "world news", "India news", "tech news", "sports news", Hindi news. Spoken summaries should stay short.

## Safety rules (do not weaken)
- The server must bind only to `127.0.0.1` and keep the Host and Origin checks.
- Always ask Allow or Deny in the interface before: shutdown, restart, lock, closing a browser, closing all tabs, or anything that deletes or sends something.
- No arbitrary command execution, no file deletion, no reading personal files.
- The AI model must never claim it did an action. Only the server's real actions count.

## Acceptance tests (run them and report Pass or Fail)
1. Say or type "open youtube and gmail". Two tabs open. Then "close it". Both tabs close.
2. "open notepad", then "close it". Notepad closes.
3. "open whatsapp" (or another installed app). It launches.
4. Say "भारत की राजधानी क्या है". The reply is spoken in Hindi, and the screen shows English.
5. Say "what is the capital of France". The reply is spoken in English.
6. "latest news" and "world news". Short spoken summaries.
7. "how fast is my internet". Reports a speed.
8. "lock the laptop" shows Allow and Deny, and does nothing until Allow.
9. Open the page and leave it idle for 1 minute. CPU use stays low and the page does not stutter.

## Deliverables
- Updated `server.py`, `index.html`, `start.bat`, `start.ps1`, the new `extension/` folder, `README.md` (team contributions placeholders stay) and `TEST-SCENARIOS.md` with a Pass or Fail column filled in.
- A short report in plain words: what works, what does not, and the exact steps for the user to start everything.
