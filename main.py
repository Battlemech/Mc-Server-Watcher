from src.mc_server_interface import MCServerInterface
import os

def main():
    # run the server until no players are online
    server = MCServerInterface()
    server.waitForExit()

    # stop the instance: it is no longer required
    os.system("sudo halt")

if __name__ == "__main__":
    main()
