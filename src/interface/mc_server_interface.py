import subprocess
import subprocess

from src.interface.server_tracker import IsServerAbandonded
from src.interface.server_commands import send_command, setup_command_sender
from src.threading_util import ensure_thread_start

def run_server(min_gb: int = 1, max_gb: int = 7, server_folder: str = '../IER Serverpack 4.3.1/'):
    try:
        # Start a subprocess with the command 'java -Xmx7G -Xms6G -jar forge-1.12.2-14.23.5.2860.jar nogui'
        # The subprocess is executed in the '/path/to/server/folder' directory
        # The stdout and stderr of the subprocess are redirected to pipes
        server_process = subprocess.Popen(['java', f'-Xmx{max_gb}G', f'-Xms6{min_gb}', '-jar', 'forge-1.12.2-14.23.5.2860.jar', 'nogui'], cwd=server_folder, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

        # allows sending commands to the server
        command_thread = setup_command_sender(server_process)

        # make sure the server is running
        ensure_thread_start(server_process)
        ensure_thread_start(command_thread)

        # Continuously read server output
        while True:
            # Read a line from the stdout pipe of the subprocess
            output = server_process.stdout.readline().decode().strip()

            # If the output is empty, the subprocess has terminated
            if not output:
                break

            # Check if all players left the server
            if IsServerAbandonded():
                break

        # Stop the server
        stop_server(server_process)
    
    # Catch any exception that occurs during the execution of the subprocess and print an error message
    except Exception as e:
        print(f'Error starting server: {str(e)}')

def stop_server(server_process: subprocess.Popen[bytes]):
    # send stop command to server
    send_command('/stop')

    # wait for server to stop
    server_process.wait()