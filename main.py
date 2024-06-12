from src.mc_server_interface import MCServerInterface
import os
from datetime import datetime

def main():
    # create a simple log file, printing current time
    with open("log.txt", "w") as log:
        log.write(f"Server started at {datetime.now()}!\n")

    # run the server until no players are online
    server = MCServerInterface()
    server.waitForExit()

    # stop the instance: it is no longer required
    os.system("sudo halt")

if __name__ == "__main__":
    main()
