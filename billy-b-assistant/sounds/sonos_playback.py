import os
import threading
import http.server
import socketserver
from soco import discover

# ========== Settings ==========
AUDIO_DIR = "sounds/response-history"
HTTP_PORT = 8000
LAN_IP = "192.168.1.247"  # 🔁 Replace with your actual LAN IP

# ========== Start HTTP Server ==========
def start_http_server():
    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.chdir(AUDIO_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", HTTP_PORT), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    print(f"📡 HTTP server running at http://{LAN_IP}:{HTTP_PORT}/")

# ========== Sonos Functions ==========
def find_sonos_device():
    speakers = discover()
    if not speakers:
        print("❌ No Sonos devices found.")
        return None
    speaker = sorted(speakers, key=lambda x: x.player_name)[0]
    print(f"🔊 Using Sonos speaker: {speaker.player_name} ({speaker.ip_address})")
    return speaker

def play_audio_on_sonos(filename, speaker):
    url = f"http://{LAN_IP}:{HTTP_PORT}/{filename}"
    print(f"🎵 Sending to Sonos: {url}")
    speaker.play_uri(url)

# ========== Main Playback Function ==========
def handle_incoming_audio(audio_bytes, filename="response-1.wav"):
    path = os.path.join(AUDIO_DIR, filename)
    with open(path, "wb") as f:
        f.write(audio_bytes)

    speaker = find_sonos_device()
    if speaker:
        play_audio_on_sonos(filename, speaker)

# ========== Startup ==========
if __name__ == "__main__":
    start_http_server()

    # 🔁 Simulate incoming audio (replace with your TTS or WebSocket code)
    import time
    print("⏳ Waiting to play test audio...")
    time.sleep(2)

    # Example: play a WAV file you have saved
    with open("test.wav", "rb") as f:  # Put a valid WAV file in your project folder
        handle_incoming_audio(f.read())
