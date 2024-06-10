import subprocess
import subprocess
import time

from src.interface.server_tracker import IsServerAbandonded

def run_server(min_gb: int = 1, max_gb: int = 7, server_folder: str = '../IER Serverpack 4.3.1/'):
    # Start a subprocess with the command 'java -Xmx7G -Xms6G -jar forge-1.12.2-14.23.5.2860.jar nogui'
    # The subprocess is executed in the '/path/to/server/folder' directory
    # The stdout and stderr of the subprocess are redirected to pipes
    server_process = subprocess.Popen(['java', f'-Xmx{max_gb}G', f'-Xms{min_gb}G', '-jar', 'forge-1.12.2-14.23.5.2860.jar', 'nogui'], cwd=server_folder, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    print("Started server!")

    def server_loop():
        is_faulted = False

        # read errors
        while(server_process.stderr.readable()):
            error = server_process.stderr.readline().decode().strip()

            # server process termianted
            if not error:
                print("MC Error: Server thread terminated")
                is_faulted = True
                break

            print("MC Error:", error)

        # read standard output
        while(server_process.stdout.readable()):
            output = server_process.stdout.readline().decode().strip()

            print("MC:", output)

            # server process termianted
            if not output:
                print("MC: Server thread termianted")
                return False
            
            # prevent invalid lookups
            if is_faulted:
                print("Skipping server count lookup: Error was detected")
                return False

            if IsServerAbandonded():
                print("MC: No players remain on the server!")
                return True

        # wait for more output
        print("Waiting for more output!")
        time.sleep(1)

    # true if server is still running, otherwise false
    is_running = server_loop()

    # server is already stopped
    if not is_running:
        return

    # tell the server to stop
    server_process.stdin.write("\stop".encode() + b'\n')
    server_process.stdin.flush()

    # wait for the server to terminate
    print("Waiting for server to stop")
    server_process.wait()
    print("Server stopped")