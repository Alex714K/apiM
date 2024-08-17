import threading
import time
from plugins.cycle_init_func import launch


if __name__ == "__main__":
    main_thrd = threading.Thread(target=launch)
    main_thrd.start()
    while True:
        time.sleep(2)
        if not main_thrd.is_alive():
            main_thrd = threading.Thread(target=launch)
            main_thrd.start()
