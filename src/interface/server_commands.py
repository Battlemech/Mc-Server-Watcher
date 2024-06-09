import threading
from queue import Queue

# create q threadsafe queue which saves commands to be executed
command_queue = Queue()

def run_server_commands(server_process):
    while True:
        # get command from queue
        command = command_queue.get()
        
        # Write the command to the stdin pipe of the subprocess
        server_process.stdin.write(command.encode() + b'\n')
        server_process.stdin.flush()
        
        # Check if the server process has terminated
        if server_process.poll() is not None:
            break

def setup_command_sender(server_process):
    # Create a background thread to send commands to the server
    command_thread = threading.Thread(target=run_server_commands, args=(server_process,))
    command_thread.start()

    return command_thread
    
def send_command(command):
    # Put the command in the queue
    command_queue.put(command)