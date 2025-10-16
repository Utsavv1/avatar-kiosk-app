import threading
from avatar_main import main as run_avatar
from surveillance_app import run_surveillance

if __name__ == "__main__":
    avatar_thread = threading.Thread(target=run_avatar)
    surveillance_thread = threading.Thread(target=run_surveillance)

    avatar_thread.start()
    surveillance_thread.start()

    avatar_thread.join()
    surveillance_thread.join()
