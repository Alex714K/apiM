import schedule
from plugins.cycles.WB_cycle import WB_cycle
from plugins.cycles.Ozon_cycle import Ozon_cycle


if __name__ == "__main__":
    WB_cycle()
    Ozon_cycle()

    print(schedule.get_jobs())
    while True:
        schedule.run_pending()
