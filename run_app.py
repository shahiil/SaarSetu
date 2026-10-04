import os
import sys
import subprocess
import time

def run_kannadasaar():
    print("=" * 60)
    print("  🚀 Launching KannadaSaar Web Application & API Backend")
    print("=" * 60)

    root_dir = os.path.abspath(os.path.dirname(__file__))
    venv_python = os.path.join(root_dir, "venv", "Scripts", "python.exe") if os.name == "nt" else os.path.join(root_dir, "venv", "bin", "python")

    if not os.path.exists(venv_python):
        venv_python = sys.executable

    print("\n1. Starting FastAPI Backend Server on http://localhost:8000 ...")
    backend_process = subprocess.Popen(
        [venv_python, "-m", "uvicorn", "backend.app.main:app", "--reload", "--port", "8000"],
        cwd=root_dir
    )

    time.sleep(2)

    print("\n2. Starting React Vite Frontend Server on http://localhost:5173 ...")
    frontend_dir = os.path.join(root_dir, "frontend")
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    
    frontend_process = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=frontend_dir
    )

    print("\n" + "=" * 60)
    print("  ✅ BOTH SERVICES ARE RUNNING!")
    print("  - Web Application: http://localhost:5173")
    print("  - Backend API:     http://localhost:8000")
    print("  - Swagger API Docs: http://localhost:8000/docs")
    print("=" * 60 + "\n")

    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nStopping KannadaSaar services...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    run_kannadasaar()
