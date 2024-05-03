from Api import Api
import schedule
import logging
from cycles.WB_cycle import WB_cycle


if __name__ == "__main__":
    WB_cycle()

    print(schedule.get_jobs())
    while True:
        schedule.run_pending()
