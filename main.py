from Api import Api


if __name__ == "__main__":
    API = Api()
    # API.start('stocks', dateFrom='today')
    # API.start('orders_1mnth', dateFrom='1mnth')
    # API.start('orders_1week', dateFrom='1week')
    # API.start('orders_2days', dateFrom='2days')
    # API.start('orders_today', dateFrom='today', flag='1')
    # API.start('tariffs_boxes', date='today')
    # API.start('tariffs_pallet', date='today')
    API.start('goods', filterNmID='')
