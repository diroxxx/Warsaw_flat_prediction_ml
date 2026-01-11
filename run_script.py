"""
Script to start and manage API and Streamlit processes.
"""

import sys
import subprocess
import time

CMD_API = [sys.executable, "-m", "uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8008", "--reload"]
CMD_STREAMLIT = [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"]

def start_process(cmd):
    return subprocess.Popen(cmd)

def stop_process(p):
    if p and p.poll() is None:
        try:
            p.terminate()
        except Exception:
            pass
        time.sleep(1)
        if p.poll() is None:
            try:
                p.kill()
            except Exception:
                pass

def main():
    p_api = start_process(CMD_API)
    p_streamlit = start_process(CMD_STREAMLIT)
    try:
        while True:
            time.sleep(1)
            if p_api.poll() is not None or p_streamlit.poll() is not None:
                break
    except KeyboardInterrupt:
        pass
    finally:
        stop_process(p_streamlit)
        stop_process(p_api)
        print("Zakończono procesy.")

if __name__ == "__main__":
    main()