from src.instance_stopper import stop_instance
from src.interface.mc_server_interface import run_server

def main():
    # run the server until no players are online
    run_server()

    # stop the instance: it is no longer required
    # stop_instance()

if __name__ == "__main__":
    main()
