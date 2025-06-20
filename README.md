# 🎧 Lo-Fi Radio Monitor Bot

A fun DevOps + Python mini project that checks if a Lo-Fi YouTube stream is online, logs uptime, and displays everything in a dark-themed dashboard with a real-time graph, thumbnails, and Discord alerts.

## 🚀 Features

- FastAPI-powered web dashboard
- Real-time uptime chart (Chart.js)
- YouTube thumbnails
- Discord webhook alerts
- Dark mode UI
- Manual re-check button
- Stream status logging (`uptime_log.csv`)

## 📦 Tech Stack

- Python + FastAPI
- Jinja2 Templates
- Chart.js
- Discord Webhooks
- GitHub + VS Code

## 🖥️ How to Run

```bash
git clone https://github.com/YOUR_USERNAME/lofi-radio-monitor.git
cd lofi-radio-monitor
python -m venv .venv
source .venv/Scripts/activate  # or 'source .venv/bin/activate' on Mac/Linux
pip install -r requirements.txt
python run_this.py
