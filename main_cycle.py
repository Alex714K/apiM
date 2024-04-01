from Api import Api
import schedule
import logging


if __name__ == "__main__":
    API = Api()
    schedule.every(1).day.at("04:45").do(API.start, name_of_sheet='stocks', dateFrom='today')
    schedule.every(1).day.at("04:50").do(API.start, name_of_sheet='orders_1mnth', dateFrom='1mnth')
    schedule.every(1).day.at("04:55").do(API.start, name_of_sheet='orders_1week', dateFrom='1week')
    schedule.every(1).day.at("05:00").do(API.start, name_of_sheet='orders_2days', dateFrom='2days')
    schedule.every(1).day.at("05:05").do(API.start, name_of_sheet='orders_today', dateFrom='today', flag='1')
    schedule.every(1).day.at("05:10").do(API.start, name_of_sheet='tariffs_boxes', date='tariffs')
    schedule.every(1).day.at("05:15").do(API.start, name_of_sheet='tariffs_pallet', date='tariffs')
    schedule.every().wednesday.at("17:00").do(API.start, name_of_sheet='statements', dateFrom='tariffs')
    schedule.every(30).minutes.do(API.start, name_of_sheet='prices', limit='1000', filterNmID='')
    print(schedule.get_jobs())
    while True:
        schedule.run_pending()
