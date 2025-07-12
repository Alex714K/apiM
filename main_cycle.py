import threading
import time

from plugins.Api import Api
from plugins.cycle_init_func import launch
from plugins.manual_full_update import manual_full_update

if __name__ == "__main__":
    # launch()
    api = Api()
    while True:
        manual_full_update(api)