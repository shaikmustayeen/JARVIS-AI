$s = Read-Host "Paste your Gemini API key (it stays hidden)" -AsSecureString
$env:GEMINI_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s))
Start-Process "http://127.0.0.1:8765"
python "$PSScriptRoot\server.py"
