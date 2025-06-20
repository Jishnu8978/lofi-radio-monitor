import requests
import os
import time
import random
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import csv
import re
import json

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

# === FastAPI Setup ===
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

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

def read_log():
    entries = []
    try:
        with open(LOG_FILE, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reversed(list(reader)):
                entries.append({"time": row[0], "url": row[1], "status": row[2]})
    except FileNotFoundError:
        pass
    return entries

def extract_video_id(url):
    match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11})(?:[?&]|$)", url)
    return match.group(1) if match else None

def get_status_counts(logs):
    up, down = 0, 0
    for row in logs:
        if row['status'] == 'UP':
            up += 1
        else:
            down += 1
    return up, down

# === Web Routes ===
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    logs = read_log()
    chart_data = {"labels": [], "data": []}
    for entry in logs[-50:][::-1]:
        chart_data["labels"].append(entry['time'])
        chart_data["data"].append(1 if entry['status'] == "UP" else 0)
    chart_json = json.dumps(chart_data)
    up, down = get_status_counts(logs)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "logs": logs,
        "chart_json": chart_json,
        "up": up,
        "down": down
    })

@app.post("/check")
def manual_check():
    previous_status = load_previous_status()
    current_status = {}

    for url in URLS:
        is_up = check_stream(url)
        log_status(url, is_up)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_text = "UP" if is_up else "DOWN"
        current_status[url] = status_text

        if url not in previous_status:
            continue

        if previous_status[url] != status_text:
            if is_up:
                send_alert(f"✅ Stream is BACK ONLINE at {now}: {url}")
            else:
                quote = random.choice(CHILL_QUOTES)
                send_alert(f"🔴 Stream is DOWN at {now}: {url}\n💬 {quote}")

        print(f"[{now}] {url} is {status_text}")

    save_current_status(current_status)
    return RedirectResponse(url="/", status_code=303)

# === Script Entry Point ===
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

        if previous_status[url] != status_text:
            if is_up:
                send_alert(f"✅ Stream is BACK ONLINE at {now}: {url}")
            else:
                quote = random.choice(CHILL_QUOTES)
                send_alert(f"🔴 Stream is DOWN at {now}: {url}\n💬 {quote}")

        print(f"[{now}] {url} is {status_text}")

    save_current_status(current_status)
