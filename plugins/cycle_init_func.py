import schedule
from plugins.cycles.WB_cycle import WB_cycle
from plugins.cycles.Ozon_cycle import Ozon_cycle


def launch():
    WB_cycle()
    Ozon_cycle()

    while True:
        schedule.run_pending()
