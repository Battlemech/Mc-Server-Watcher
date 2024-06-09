from src.instance_stopper import stop_instance
from src.interface.mc_server_interface import run_server

def main():
    try:
        # run the server until no players are online
        run_server()

        # stop the instance: it is no longer required
        stop_instance()
    except Exception as e:
        print(f'Error starting server: {str(e)}')

if __name__ == "__main__":
    main()
