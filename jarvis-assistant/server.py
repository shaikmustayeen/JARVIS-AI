"""Jarvis backend. Run: python server.py  (Windows). Only listens on this laptop."""
import json, os, re, secrets, subprocess, time, urllib.request, urllib.error, webbrowser
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote_plus

PORT = 8765
ROOT = Path(__file__).parent
KEY = os.environ.get("GEMINI_API_KEY", "")
BASE = os.environ.get("LLM_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/").rstrip("/")
MODEL = os.environ.get("LLM_MODEL", "gemini-flash-lite-latest")
HOSTS = {f"127.0.0.1:{PORT}", f"localhost:{PORT}"}
HI = "[\u0900-\u097F]"
NOWIN = 0x08000000
pending, last = {}, {"apps": [], "tab": False}

APPS = {"notepad": "notepad", "नोटपैड": "notepad", "calculator": "calc", "कैलकुलेटर": "calc", "paint": "mspaint",
        "chrome": "chrome", "क्रोम": "chrome", "edge": "msedge", "explorer": "explorer", "word": "winword",
        "excel": "excel", "settings": "ms-settings:", "सेटिंग": "ms-settings:", "camera": "microsoft.windows.camera:",
        "कैमरा": "microsoft.windows.camera:", "task manager": "taskmgr", "snipping tool": "snippingtool",
        "control panel": "control", "vs code": "code", "vscode": "code", "firefox": "firefox", "brave": "brave",
        "downloads": "shell:Downloads", "documents": "shell:Personal"}
SITES = {"youtube": "https://www.youtube.com", "यूट्यूब": "https://www.youtube.com", "google": "https://www.google.com",
         "गूगल": "https://www.google.com", "gmail": "https://mail.google.com", "github": "https://github.com",
         "whatsapp": "https://web.whatsapp.com", "maps": "https://maps.google.com", "chatgpt": "https://chatgpt.com",
         "claude": "https://claude.ai", "gemini": "https://gemini.google.com", "instagram": "https://www.instagram.com",
         "facebook": "https://www.facebook.com", "linkedin": "https://www.linkedin.com", "netflix": "https://www.netflix.com",
         "spotify": "https://open.spotify.com", "amazon": "https://www.amazon.in", "flipkart": "https://www.flipkart.com",
         "telegram": "https://web.telegram.org", "reddit": "https://www.reddit.com", "stackoverflow": "https://stackoverflow.com",
         "drive": "https://drive.google.com", "calendar": "https://calendar.google.com",
         "outlook": "https://outlook.office.com", "classroom": "https://classroom.google.com"}
# apps Jarvis may close: name -> (process, force)
PROC = {"notepad": ("notepad.exe", 0), "नोटपैड": ("notepad.exe", 0), "calculator": ("CalculatorApp.exe", 1),
        "कैलकुलेटर": ("CalculatorApp.exe", 1), "paint": ("mspaint.exe", 0), "settings": ("SystemSettings.exe", 1),
        "सेटिंग": ("SystemSettings.exe", 1), "camera": ("WindowsCamera.exe", 1), "कैमरा": ("WindowsCamera.exe", 1),
        "snipping tool": ("SnippingTool.exe", 1), "word": ("WINWORD.EXE", 0), "excel": ("EXCEL.EXE", 0),
        "vs code": ("Code.exe", 0), "vscode": ("Code.exe", 0), "firefox": ("firefox.exe", 0)}
BROWSERS = {"chrome": "chrome.exe", "क्रोम": "chrome.exe", "edge": "msedge.exe", "brave": "brave.exe"}
DOMAIN = r"\b([a-z0-9-]+\.(?:com|in|org|net|io|ai|co|app|edu|gov))\b"
OPEN = r"\b(open|launch|start|go to)\b|खोलो|खोल|चालू|kholo"
TABKEY = ["powershell", "-NoProfile", "-Command", "Start-Sleep 3; $w=New-Object -ComObject WScript.Shell; $w.SendKeys('^w')"]


def has(t, name):
    if re.search(HI, name): return name in t
    return re.search(r"(?<![a-z0-9])" + re.escape(name) + r"(?![a-z0-9])", t) is not None


def vol(key):
    return ["powershell", "-NoProfile", "-Command", f"$w=New-Object -ComObject WScript.Shell;1..5|%{{$w.SendKeys([char]{key})}}"]


def yt_first(q):
    """Open the first YouTube result for q (falls back to the results page)."""
    try:
        req = urllib.request.Request("https://www.youtube.com/results?search_query=" + quote_plus(q),
                                     headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en"})
        html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "ignore")
        m = re.search(r'"videoId":"([\w-]{11})"', html)
        if m: return "https://www.youtube.com/watch?v=" + m.group(1) + "&autoplay=1"
    except Exception:
        pass
    return "https://www.youtube.com/results?search_query=" + quote_plus(q)


def parse(text):
    """Return None, or (risky, english, hindi, kind, target)."""
    t = text.lower()
    if re.search(r"shut ?down|शट ?डाउन", t):
        return (True, "Shut down the laptop in 30 seconds?", "30 सेकंड में लैपटॉप बंद करूँ?", "cmd", ["shutdown", "/s", "/t", "30"])
    if re.search(r"restart|रीस्टार्ट|रिस्टार्ट", t):
        return (True, "Restart the laptop in 30 seconds?", "30 सेकंड में लैपटॉप रीस्टार्ट करूँ?", "cmd", ["shutdown", "/r", "/t", "30"])
    if re.search(r"\block\b|लॉक", t):
        return (True, "Lock the laptop?", "लैपटॉप लॉक करूँ?", "cmd", ["rundll32.exe", "user32.dll,LockWorkStation"])
    if re.search(r"volume|awaz|आवाज", t):
        if re.search(r"up|increase|badha|बढ़ा", t): return (False, "Volume up.", "आवाज़ बढ़ा दी।", "cmd", vol(175))
        if re.search(r"down|decrease|kam|घटा|कम", t): return (False, "Volume down.", "आवाज़ कम कर दी।", "cmd", vol(174))
        if re.search(r"mute|band|बंद|म्यूट", t): return (False, "Muted.", "म्यूट कर दिया।", "cmd", vol(173))
    if re.search(r"\b(close|quit|exit)\b|बंद कर", t):
        pron = re.search(r"\b(it|that|this|them)\b", t)
        if re.search(r"\btabs?\b|टैब", t) or (pron and last["tab"] and not last["apps"]):
            return (True, "Close the active browser tab in 3 seconds? Click the tab you want closed now.",
                    "3 सेकंड में सक्रिय टैब बंद करूँ? जो टैब बंद करना है उस पर क्लिक कीजिए।", "cmd", TABKEY)
        for name, exe in BROWSERS.items():
            if has(t, name):
                return (True, f"Close ALL {name} windows and tabs?", f"{name} की सारी विंडो और टैब बंद करूँ?", "cmd", ["taskkill", "/IM", exe])
        hits = [(n, p) for n, p in PROC.items() if has(t, n)]
        if not hits and pron: hits = [(a, PROC[a]) for a in last["apps"] if a in PROC]
        if hits:
            names = ", ".join(n for n, _ in hits)
            return (False, f"Closing {names}.", f"{names} बंद कर रहा हूँ।", "multi",
                    [("cmd", ["taskkill", "/IM", p[0]] + (["/F"] if p[1] else [])) for _, p in hits])
    m = re.search(r"search\s+(?:for\s+)?(.+?)\s+and\s+play", t) or re.search(r"(?:\bplay|चलाओ|चला)\s+(.+?)(?:\s+on youtube|\s+यूट्यूब पर)?$", t)
    if m:
        q = m.group(1).strip()
        return (False, f"Playing the first YouTube result for {q}.", f"यूट्यूब पर {q} चला रहा हूँ।", "url", yt_first(q))
    opening = re.search(OPEN, t)
    m = None if opening else re.search(r"(?:search|google|सर्च|खोजो)\s+(?:for\s+|on google\s+)?(.+)", t)
    if m:
        q = re.sub(r"\s*(पर|on google)$", "", m.group(1)).strip()
        return (False, f"Searching Google for {q}.", f"गूगल पर {q} खोज रहा हूँ।", "url", "https://www.google.com/search?q=" + quote_plus(q))
    if opening:
        domains = re.findall(DOMAIN, t)
        t2 = re.sub(DOMAIN, " ", t)
        acts, names = [("url", "https://" + d) for d in domains], list(domains)
        for name, target in APPS.items():
            if has(t2, name): acts.append(("cmd", ["cmd", "/c", "start", "", target])); names.append(name)
        for name, url in SITES.items():
            if has(t2, name): acts.append(("url", url)); names.append(name)
        if acts:
            last["apps"] = [n for n in names if n in PROC]
            last["tab"] = any(k == "url" for k, _ in acts)
            n = ", ".join(names)
            return (False, f"Opening {n}.", f"{n} खोल रहा हूँ।", "multi", acts)
        q = re.sub(OPEN + r"|\b(the|app|website|please|jarvis)\b", " ", t).strip()
        if q:
            return (False, f"I do not know {q}, so I am searching Google.", f"{q} नहीं पता, गूगल पर खोज रहा हूँ।",
                    "url", "https://www.google.com/search?q=" + quote_plus(q))
    return None


def execute(kind, target):
    if kind == "multi":
        for k, tg in target: execute(k, tg)
    elif kind == "url": webbrowser.open(target)
    else: subprocess.Popen(target, creationflags=NOWIN)


def speedtest():
    req = urllib.request.Request("https://speed.cloudflare.com/__down?bytes=20000000", headers={"User-Agent": "Mozilla/5.0"})
    t0, n = time.time(), 0
    with urllib.request.urlopen(req, timeout=40) as r:
        while True:
            b = r.read(65536)
            if not b: break
            n += len(b)
    return round(n * 8 / (time.time() - t0) / 1e6, 1)


def llm(msgs):
    req = urllib.request.Request(BASE + "/chat/completions", json.dumps({"model": MODEL, "messages": msgs}).encode(),
                                 {"Content-Type": "application/json", "Authorization": "Bearer " + KEY})
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError:
            raise
        except Exception:
            if attempt == 2: raise


def err(e):
    if isinstance(e, urllib.error.HTTPError):
        if e.code == 429: return "The free limit is used up for now. Try again later."
        if e.code in (400, 401, 403): return "The AI service refused the key. Check that the Gemini key is correct."
        return f"The AI service returned error {e.code}."
    return "I could not reach the AI service. Check your internet."


def ask_llm(text, hist, extra=""):
    """Return (spoken, shown_on_screen, user_words_in_english)."""
    if not KEY:
        m = "No API key found. Close the program, start it with start.bat, and paste your Gemini key."
        return m, m, ""
    hi = bool(re.search(HI, text))
    sysmsg = ("You are Jarvis, a calm, polite voice assistant for Tanveer. Answer any question like a knowledgeable search assistant. "
              "Reply in the same language as the user: Hindi in Devanagari script, or English. Keep answers short and in plain words "
              "because they are spoken aloud (at most 4 sentences unless asked for more). If you are not sure, say so; never invent facts. "
              "You cannot open apps or websites or lock the computer yourself, and you must never claim you did; the program does "
              "that when it understands a command. If asked, say you did not catch the command and give an example like 'open YouTube'. "
              + (("Fresh news headlines from Google News, fetched just now: " + extra + " Summarize only from these headlines. ") if extra else "")
              + "Current date and time: " + time.strftime("%A, %d %B %Y, %I:%M %p"))
    if hi:
        sysmsg += (" The user spoke Hindi. Output exactly three parts separated by the token ||| and nothing else: "
                   "(1) the user's words translated to English, (2) your answer in Hindi (Devanagari) for speaking aloud, "
                   "(3) the same answer in English for the screen.")
    msgs = [{"role": "system", "content": sysmsg}]
    msgs += [{"role": h["role"], "content": str(h["content"])} for h in hist[-8:] if h.get("role") in ("user", "assistant")]
    msgs.append({"role": "user", "content": text})
    try:
        out = llm(msgs)
    except Exception as e:
        m = err(e)
        return m, m, ""
    if hi:
        p = [x.strip() for x in out.split("|||")]
        if len(p) >= 3: return p[1], p[2], p[0]
    return out, out, ""


def headlines(text, hi):
    """Fetch fresh headlines from Google News (no key needed)."""
    t = text.lower()
    topic = re.sub(r"\b(latest|live|today'?s?|give|tell|me|the|news|headlines|about|on|of|for|what'?s|what|is|are|"
                   r"happening|in|please|any|some|jarvis)\b|खबर\w*|समाचार|न्यूज़?|आज|ताज़ा|ताजा|बताओ|सुनाओ", " ", t)
    topic = " ".join(topic.split())
    loc = "hl=hi&gl=IN&ceid=IN:hi" if hi else "hl=en-IN&gl=IN&ceid=IN:en"
    url = "https://news.google.com/rss" + ("/search?q=" + quote_plus(topic) + "&" if topic else "?") + loc
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            items = ET.fromstring(r.read()).iter("item")
            return "\n".join("- " + i.findtext("title", "") for _, i in zip(range(6), items))
    except Exception:
        return ""


def say(en, hin, hi):
    return {"type": "answer", "reply": hin if hi else en, "text": en}


def chat(d):
    text = (d.get("text") or "").strip()
    hi = bool(re.search(HI, text))
    tl = text.lower()
    if re.search(r"speed|fast|स्पीड", tl) and re.search(r"\bnet\b|internet|wifi|wi-fi|इंटरनेट|नेट|test", tl):
        try: s = speedtest()
        except Exception: return say("I could not run the speed test. Check your internet.", "स्पीड टेस्ट नहीं हो पाया। इंटरनेट जाँचिए।", hi)
        return say(f"Your download speed is about {s} megabits per second.", f"आपकी डाउनलोड स्पीड लगभग {s} मेगाबिट प्रति सेकंड है।", hi)
    if re.search(r"\bnews\b|headlines|खबर|समाचार|न्यूज", tl) and not re.search(r"\b(open|launch)\b|खोलो", tl):
        h = headlines(text, hi)
        if not h: return say("I could not fetch the news right now. Check your internet.", "अभी खबरें नहीं मिल पाईं। इंटरनेट जाँचिए।", hi)
        a, b, c = ask_llm("Give a short spoken news briefing for: " + text, [], h)
        return {"type": "answer", "reply": a, "text": b, "heard": c}
    act = parse(text)
    if not act:
        a, b, c = ask_llm(text, d.get("history") or [])
        return {"type": "answer", "reply": a, "text": b, "heard": c}
    risky, en, hin, kind, target = act
    if risky:
        tok = secrets.token_urlsafe(8)
        pending[tok] = (kind, target, hi)
        r = say(en, hin, hi); r.update(type="confirm", token=tok)
        return r
    execute(kind, target)
    if kind == "url": last.update(apps=[], tab=True)
    return say(en, hin, hi)


def run(d):
    p = pending.pop(d.get("token", ""), None)
    if not p: return {"type": "answer", "reply": "That request expired.", "text": "That request expired."}
    execute(p[0], p[1])
    return say("Done.", "ठीक है, कर दिया।", p[2])


def listen(d):
    """Turn recorded audio (wav, base64) into text with the same AI service."""
    if not KEY: return {"text": "", "error": "No API key. Start with start.bat."}
    ask = ("Transcribe this audio exactly. The speaker uses English or Hindi (write Hindi in Devanagari). "
           "Output only the spoken words and nothing else. If there is no speech, output nothing.")
    try:
        out = llm([{"role": "user", "content": [{"type": "text", "text": ask},
                   {"type": "input_audio", "input_audio": {"data": d.get("audio", ""), "format": "wav"}}]}])
        return {"text": out}
    except Exception as e:
        return {"text": "", "error": err(e)}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass

    def send(self, code, body, ctype="application/json"):
        b = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code); self.send_header("Content-Type", ctype + "; charset=utf-8")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def allowed(self):
        o = self.headers.get("Origin")
        return self.headers.get("Host") in HOSTS and (not o or o in {"http://" + h for h in HOSTS})

    def do_GET(self):
        if not self.allowed(): return self.send(403, {"error": "forbidden"})
        if self.path in ("/", "/index.html"): return self.send(200, (ROOT / "index.html").read_bytes(), "text/html")
        self.send(404, {"error": "not found"})

    def do_POST(self):
        if not self.allowed(): return self.send(403, {"error": "forbidden"})
        try:
            d = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            fn = {"/api/chat": chat, "/api/run": run, "/api/listen": listen}.get(self.path)
            out = fn(d) if fn else None
        except Exception:
            out = {"type": "answer", "reply": "Something went wrong inside the server.", "text": "Something went wrong inside the server."}
        self.send(200 if out else 404, out or {"error": "not found"})


if __name__ == "__main__":
    print(f"Jarvis is running at http://127.0.0.1:{PORT}  (press Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
