#!/usr/bin/env python3
"""
Run both frontend and backend locally for development.
This script starts the NextJS frontend and FastAPI backend in parallel.
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

# Track subprocesses for cleanup
processes = []

def cleanup(signum=None, frame=None):
    """Clean up all subprocess on exit"""
    print("\n🛑 Shutting down services...")
    for proc in processes:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except:
            proc.kill()
    sys.exit(0)

# Register cleanup handlers
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def check_requirements():
    """Check if required tools are installed"""
    checks = []

    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        node_version = result.stdout.strip()
        checks.append(f"✅ Node.js: {node_version}")
    except FileNotFoundError:
        checks.append("❌ Node.js not found - please install Node.js")

    # Check npm
    try:
        # shell=True eklendiğinde Windows npm.cmd'yi otomatik bulur
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            npm_version = result.stdout.strip()
            checks.append(f"✅ npm: {npm_version}")
        else:
            checks.append("❌ npm found but returned an error")
    except FileNotFoundError:
        checks.append("❌ npm not found - please install npm")

    # Check uv (which manages Python for us)
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        uv_version = result.stdout.strip()
        checks.append(f"✅ uv: {uv_version}")
    except FileNotFoundError:
        checks.append("❌ uv not found - please install uv")

    print("\n📋 Prerequisites Check:")
    for check in checks:
        print(f"  {check}")

    # Exit if any critical tools are missing
    if any("❌" in check for check in checks):
        print("\n⚠️  Please install missing dependencies and try again.")
        sys.exit(1)

def check_env_files():
    """Check if environment files exist"""
    project_root = Path(__file__).parent.parent

    root_env = project_root / ".env"
    frontend_env = project_root / "frontend" / ".env.local"

    missing = []

    if not root_env.exists():
        missing.append(".env (root project file)")
    if not frontend_env.exists():
        missing.append("frontend/.env.local")

    if missing:
        print("\n⚠️  Missing environment files:")
        for file in missing:
            print(f"  - {file}")
        print("\nPlease create these files with the required configuration.")
        print("The root .env should have all backend variables from Parts 1-7.")
        print("The frontend/.env.local should have Clerk keys.")
        sys.exit(1)

    print("✅ Environment files found")

def start_backend():
    """Start the FastAPI backend"""
    backend_dir = Path(__file__).parent.parent / "backend" / "api"

    print("\n🚀 Starting FastAPI backend...")

    # Check if dependencies are installed
    if not (backend_dir / ".venv").exists() and not (backend_dir / "uv.lock").exists():
        print("  Installing backend dependencies...")
        subprocess.run(["uv", "sync"], cwd=backend_dir, check=True)

    # Start the backend
    proc = subprocess.Popen(
        ["uv", "run", "main.py"],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    processes.append(proc)

    # Wait for backend to start
    print("  Waiting for backend to start...")
    for _ in range(30):  # 30 second timeout
        try:
            import httpx
            response = httpx.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("  ✅ Backend running at http://localhost:8000")
                print("     API docs: http://localhost:8000/docs")
                return proc
        except:
            time.sleep(1)

    print("  ❌ Backend failed to start")
    cleanup()

def start_frontend():
    """Start the NextJS frontend"""
    frontend_dir = Path(__file__).parent.parent / "frontend"

    print("\n🚀 Starting NextJS frontend...")

    # Check if dependencies are installed
    if not (frontend_dir / "node_modules").exists():
        print("   Installing frontend dependencies...")
        # Windows için shell=True kritik
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True, shell=True)

    # Start the frontend
    # stdout=subprocess.PIPE yerine stdout=None yaparak logları doğrudan terminale verebilir 
    # veya aşağıdaki gibi boruyu manuel boşaltabiliriz.
    proc = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        text=True,
        bufsize=1
    )
    processes.append(proc)

    # Wait for frontend to start
    print("   Waiting for frontend to start...")
    import httpx
    import os

    # Windows'ta borunun dolup kilitlenmesini önlemek için 
    # stdout'u bir dosyaya veya çöpe yönlendirmek daha sağlıklıdır 
    # ama bu döngüde manuel okuyacağız.
    if os.name == 'nt':
        import msvcrt
        # Boruyu non-blocking yapamayacağımız için httpx kontrolüne odaklanıyoruz

    for i in range(45):  # 45 saniye daha güvenli (NextJS 15 biraz yavaş açılabilir)
        # HTTP Kontrolü
        try:
            with httpx.Client() as client:
                # timeout=0.1 gibi çok düşük değerler yerine 
                # sadece bağlantıyı kontrol edip beklemeyi döngüye bırakıyoruz
                response = client.get("http://localhost:3000", timeout=2.0)
                print("   ✅ Frontend running at http://localhost:3000")
                return proc
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout):
            # Sunucu ya henüz yok (Connect) ya da çok meşgul (ReadTimeout)
            # Bu hataları yutarak döngünün devam etmesini sağlıyoruz
            pass
        
        # Süreci kontrol et: Erken kapandıysa hata ver
        if proc.poll() is not None:
            print("   ❌ Frontend process exited unexpectedly")
            break

        if i % 5 == 0:
            print(f"   ... still waiting ({i}s)")
            
        time.sleep(1)

    print("   ❌ Frontend failed to start or timed out")
    cleanup()
    sys.exit(1)

def monitor_processes():
    """Monitor running processes and show their output"""
    print("\n" + "="*60)
    print("🎯 Alex Financial Advisor - Local Development")
    print("="*60)
    print("\n📍 Services:")
    print("  Frontend: http://localhost:3000")
    print("  Backend:  http://localhost:8000")
    print("  API Docs: http://localhost:8000/docs")
    print("\n📝 Logs will appear below. Press Ctrl+C to stop.\n")
    print("="*60 + "\n")

    # Monitor processes
    while True:
        for proc in processes:
            # Check if process is still running
            if proc.poll() is not None:
                print(f"\n⚠️  A process has stopped unexpectedly!")
                cleanup()

            # Read any available output
            try:
                line = proc.stdout.readline()
                if line:
                    print(f"[LOG] {line.strip()}")
            except:
                pass

        time.sleep(0.1)

def main():
    """Main entry point"""
    print("\n🔧 Alex Financial Advisor - Local Development Setup")
    print("="*50)

    # Check prerequisites
    check_requirements()
    check_env_files()

    # Install httpx if needed
    try:
        import httpx
    except ImportError:
        print("\n📦 Installing httpx for health checks...")
        subprocess.run(["uv", "add", "httpx"], check=True)

    # Start services
    backend_proc = start_backend()
    frontend_proc = start_frontend()

    # Monitor processes
    try:
        monitor_processes()
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()