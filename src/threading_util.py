def ensure_thread_start(process):
    # Check the return code of the subprocess
    if process.returncode == 0:
        return True
    else:
        stderr = process.stderr.read().decode().strip()
        
        if stderr:
            return str(stderr)

        return False