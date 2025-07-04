import subprocess

def run_winapi_click(window, x, y):
    command = f'winapi\\winapi.exe --click --window "{window}" -x {x} -y {y}'
    
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Clicked at {x}, {y}")
        if result.stdout:
            print("Output:", result.stdout.decode('utf-8'))
        if result.stderr:
            print("Error Output:", result.stderr.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stdout:
            print("Output:", e.stdout.decode('utf-8'))
        if e.stderr:
            print("Error Output:", e.stderr.decode('utf-8'))
    except Exception:
        print("An error occurred")
