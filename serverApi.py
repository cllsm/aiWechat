import subprocess

def start_service():
    command = ["pm2", "start", "./qwen-free-api/dist/index.js", "--name", "qwen-free-api"]
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error starting service: {e}")
        return False

def reload_service():
    command = ["pm2", "reload", "qwen-free-api"]
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error reloading service: {e}")
        return False

def stop_service():
    command = ["pm2", "stop", "qwen-free-api"]
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error stopping service: {e}")
        return False
start_service()