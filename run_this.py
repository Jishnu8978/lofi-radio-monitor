import os
import webbrowser
import subprocess
import time
import platform

def activate_venv_and_run():
    os_name = platform.system()

    # Activate virtualenv
    if os_name == "Windows":
        activate_cmd = ".venv\\Scripts\\activate.bat && "
    else:
        activate_cmd = "source .venv/bin/activate && "

    # Run Uvicorn
    run_cmd = activate_cmd + "uvicorn monitor:app --reload"

    # Start in terminal
    subprocess.Popen(run_cmd, shell=True)

    # Wait briefly and open in browser
    time.sleep(2)
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    print("🚀 Starting Lo-Fi Monitor Bot Dashboard...")
    activate_venv_and_run()
