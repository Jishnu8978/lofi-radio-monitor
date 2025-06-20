import requests
import os
import time
import random
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# === Config ===
URLS = [
    "https://www.youtube.com/@lofigirl/live",
    # Add more YouTube live URLs here
]
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
LOG_FILE = "uptime_log.csv"
STATUS_CACHE = "status_cache.txt"

# === Chill Quotes ===
CHILL_QUOTES = [
    "Take a deep breath, it’ll be back soon.",
    "Maybe it’s a sign to take a walk.",
    "Time to vibe with the silence.",
    "The lo-fi gods are just on a break.",
    "No beats? Make your own rhythm today."
]

# === Functions ===
def send_alert(message):
    payload = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK, json=payload)
        if response.status_code != 204:
            print("Failed to send alert:", response.text)
    except Exception as e:
        print("Error sending alert:", e)


def check_stream(url):
    try:
        res = requests.get(url, timeout=10)
        is_live = "LIVE NOW" in res.text or "live-streaming" in res.text.lower()
        return is_live
    except Exception as e:
        print(f"Error checking stream {url}: {e}")
        return False


def log_status(url, is_up):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "UP" if is_up else "DOWN"
    with open(LOG_FILE, "a") as f:
        f.write(f"{now},{url},{status}\n")


def load_previous_status():
    try:
        with open(STATUS_CACHE, "r") as f:
            return dict(line.strip().split("|", 1) for line in f)
    except:
        return {}


def save_current_status(status_dict):
    with open(STATUS_CACHE, "w") as f:
        for url, status in status_dict.items():
            f.write(f"{url}|{status}\n")


# === Main ===
if __name__ == "__main__":
    previous_status = load_previous_status()
    current_status = {}

    for url in URLS:
        is_up = check_stream(url)
        log_status(url, is_up)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_text = "UP" if is_up else "DOWN"
        current_status[url] = status_text

        if url not in previous_status:
            print(f"First time checking: {url} is {status_text}")
            continue

        # If status changed from previous
        if previous_status[url] != status_text:
            if is_up:
                send_alert(f"✅ Stream is BACK ONLINE at {now}: {url}")
            else:
                quote = random.choice(CHILL_QUOTES)
                send_alert(f"🔴 Stream is DOWN at {now}: {url}\n💬 {quote}")

        print(f"[{now}] {url} is {status_text}")

    save_current_status(current_status)
