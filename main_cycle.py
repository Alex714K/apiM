from Api import Api
import schedule


if __name__ == "__main__":
    schedule.every().day.at("5:00").do(Api().start())
    while True:
        schedule.run_pending()
