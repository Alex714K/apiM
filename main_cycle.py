# from Api_old import Api
from Api import Api
import schedule
import logging


if __name__ == "__main__":
    API = Api()
    # with open('schedules.txt', 'r') as txt:
    #     data = list(map(lambda x: x.split(';'), txt.read().split('\n')))
    # data = list(map(lambda x: dict(map(lambda y: y.split('='), x)), data))
    # for i in data:
    #     schedule.every().day.at(i['time']).do(API.start, )
    schedule.every().day.at("04:45").do(API.start, 'planeta', 'WB', name_of_sheet='stocks', dateFrom='2019-06-20')
    schedule.every().day.at("04:50").do(API.start, 'planeta', 'WB', name_of_sheet='orders_1mnth', dateFrom='1mnth')
    schedule.every().day.at("04:55").do(API.start, 'planeta', 'WB', name_of_sheet='orders_1week', dateFrom='1week')
    schedule.every().day.at("05:00").do(API.start, 'planeta', 'WB', name_of_sheet='orders_2days', dateFrom='2days')
    schedule.every().day.at("05:05").do(API.start, 'planeta', 'WB', name_of_sheet='orders_today', dateFrom='today', flag='1')
    schedule.every().day.at("05:10").do(API.start, 'planeta', 'WB', name_of_sheet='tariffs_boxes', date='tariffs')
    schedule.every().day.at("05:15").do(API.start, 'planeta', 'WB', name_of_sheet='tariffs_pallet', date='tariffs')
    # schedule.every().day.at("05:20").do(API.start, name_of_sheet='statements', dateFrom='statements')
    # schedule.every().day.at("05:25").do(API.start, name_of_sheet='storage_paid', dateFrom='storage_paid')
    schedule.every(30).minutes.do(API.start, 'planeta', 'WB', name_of_sheet='prices', limit='1000')
    schedule.every().day.at("13:45").do(API.start, 'planeta', 'WB', name_of_sheet='stocks', dateFrom='2019-06-20')
    schedule.every().day.at("13:50").do(API.start, 'planeta', 'WB', name_of_sheet='orders_1mnth', dateFrom='1mnth')
    schedule.every().day.at("13:55").do(API.start, 'planeta', 'WB', name_of_sheet='orders_1week', dateFrom='1week')
    schedule.every().day.at("14:00").do(API.start, 'planeta', 'WB', name_of_sheet='orders_2days', dateFrom='2days')
    schedule.every().day.at("14:05").do(API.start, 'planeta', 'WB', name_of_sheet='orders_today', dateFrom='today', flag='1')
    schedule.every().day.at("14:10").do(API.start, 'planeta', 'WB', name_of_sheet='tariffs_boxes', date='tariffs')
    schedule.every().day.at("14:15").do(API.start, 'planeta', 'WB', name_of_sheet='tariffs_pallet', date='tariffs')
    # schedule.every().day.at("14:20").do(API.start, name_of_sheet='statements', dateFrom='statements')
    # schedule.every().day.at("14:25").do(API.start, name_of_sheet='storage_paid', dateFrom='storage_paid')
    print(schedule.get_jobs())
    while True:
        schedule.run_pending()
