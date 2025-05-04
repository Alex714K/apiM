import csv
import json
import math
import pprint
import sys
import numpy
import pandas
from plugins.Ozon.Request_Ozon import RequestOzon


class Converter:
    def convert_to_list(self,
                        file: list | dict | pandas.DataFrame | str, name_of_sheet: str, who_is: str) -> \
            (tuple[list | dict, int, list | None] | str):
        """Конвертирует json-объект в список, который подходит для добавления данных из файла в Google Excel"""
        match file:
            case None:
                return "is None"
            case []:
                return "is empty"
        match name_of_sheet:
            case "analytics":
                return self.analytics(file=file)
            case "stock_on_warehouses":
                return self.stock_on_warehouses(file=file)
            case "stocks_FBS":
                return self.stocks_fbs(file=file)
            case "products":
                return self.products(file=file)
            case "prices":
                return self.prices(file=file)
            case "statistics_product":
                return self.statistics_product(file=file)
            case "orders_alt":
                return self.orders_alt(file=file)
            case "sendings":
                return self.sendings(file=file, who_is=who_is)
        if name_of_sheet in ["orders_1mnth", "orders_1week", "orders_2days"]:
            return self.orders(file)
        else:
            print(file)
            return sys.exit("I can't convert =(")

    def statistics_product(self, file: list | dict):
        keys = list(file["rows"][0].keys())
        ans = numpy.array([keys])
        for element in file["rows"]:
            values = list()
            values.extend(list(element.values()))
            values = numpy.array([values])
            ans = numpy.concatenate((ans, values), axis=0)
        needed_keys = self.check_keys(keys)
        return ans.tolist(), ans.shape[0], needed_keys

    def orders_alt(self, file: pandas.DataFrame):
        ans = [list(file.keys())]
        ans.extend(file.to_numpy().tolist())

        needed_keys = self.check_keys(list(file.keys()))

        for row in ans:
            for i_element in range(len(row)):
                if type(row[i_element]) is not str and math.isnan(row[i_element]):
                    row[i_element] = ""

        return ans, len(ans), needed_keys

    def orders(self, file: list | dict):
        keys = ["sku_id", "sku_name", "day", "ordered_units"]
        ans = numpy.array([keys])
        for row in file:
            values = list()
            dimensions = row["dimensions"]
            # добавляем dimensions
            values.append(dimensions[0]["id"])
            values.append(dimensions[0]["name"])
            values.append(dimensions[1]["id"])
            # добавляем metrics
            values.extend(row["metrics"])
            # используем numpy для быстроты программы
            values = numpy.array([values])
            ans = numpy.concatenate((ans, values), axis=0)
        needed_keys = self.check_keys(keys)
        return ans.tolist(), ans.shape[0], needed_keys

    def prices(self, file: list | dict):
        # keys = ["acquiring", "product_id", "offer_id", "currency_code", "price", "old_price", "retail_price", "vat",
        #         "min_ozon_price", "marketing_price", "marketing_seller_price", "auto_action_enabled",
        #         "external_minimal_price", "external_minimal_price_currency", "external_price_index_value",
        #         "ozon_minimal_price", "ozon_minimal_price_currency", "ozon_price_index_value", "price_index",
        #         "self_marketplaces_minimal_price", "self_marketplaces_minimal_price_currency",
        #         "self_marketplaces_price_index_value", "sales_percent", "sales_percent_fbo", "sales_percent_fbs",
        #         "fbo_fulfillment_amount", "fbo_direct_flow_trans_min_amount", "fbo_direct_flow_trans_max_amount",
        #         "fbo_deliv_to_customer_amount", "fbo_return_flow_amount", "fbo_return_flow_trans_min_amount",
        #         "fbo_return_flow_trans_max_amount", "fbs_first_mile_min_amount", "fbs_first_mile_max_amount",
        #         "fbs_direct_flow_trans_min_amount", "fbs_direct_flow_trans_max_amount", "fbs_deliv_to_customer_amount",
        #         "fbs_return_flow_amount", "fbs_return_flow_trans_min_amount", "fbs_return_flow_trans_max_amount",
        #         "volume_weight"]
        keys: list[str] = [
            "acquiring",
            "fbo_deliv_to_customer_amount",
            "fbo_direct_flow_trans_max_amount",
            "fbo_direct_flow_trans_min_amount",
            "fbo_return_flow_amount",
            "fbs_deliv_to_customer_amount",
            "fbs_direct_flow_trans_max_amount",
            "fbs_direct_flow_trans_min_amount",
            "fbs_first_mile_max_amount",
            "fbs_first_mile_min_amount",
            "fbs_return_flow_amount",
            "sales_percent_fbo",
            "sales_percent_fbs",
            "marketing_actions-current_period_from",
            "marketing_actions-current_period_to",
            "marketing_actions-ozon_actions_exist",
            "offer_id",
            "auto_action_enabled",
            "currency_code",
            "marketing_price",
            "marketing_seller_price",
            "min_price",
            "old_price",
            "price",
            "retail_price",
            "vat",
            "color_index",
            "external_index_data",
            "external_index_data",
            "external_index_data",
            "ozon_index_data",
            "ozon_index_data",
            "ozon_index_data",
            "self_marketplaces_index_data",
            "self_marketplaces_index_data",
            "self_marketplaces_index_data",
            "product_id",
            "volume_weight"
        ]
        ans = numpy.array([keys])
        for row in file:
            # "".replace(".", ",", 1)
            values = list()

            values.append(str(row["acquiring"]).replace(".", ",", 1))

            values.append(str(row["commissions"]["fbo_deliv_to_customer_amount"]).replace(".", ",", 1))
            values.append(str(row["commissions"]["fbo_direct_flow_trans_max_amount"]).replace(".", ",", 1))
            values.append(str(row["commissions"]["fbo_direct_flow_trans_min_amount"]).replace(".", ",", 1))
            values.append(str(row["commissions"]["fbo_return_flow_amount"]).replace(".", ",", 1))
            values.append(str(row["commissions"]["fbs_deliv_to_customer_amount"]).replace(".", ",", 1))
            values.append(str(row["commissions"]["fbs_direct_flow_trans_max_amount"]).replace(".", ",", 1))
            values.append(str(row["commissions"]["fbs_direct_flow_trans_min_amount"]).replace(".", ",", 1))
            values.append(str(row["commissions"]["fbs_first_mile_max_amount"]).replace(".", ",", 1))
            values.append(str(row["commissions"]["fbs_first_mile_min_amount"]).replace(".", ",", 1))
            values.append(str(row["commissions"]["fbs_return_flow_amount"]).replace(".", ",", 1))
            values.append(str(row["commissions"]["sales_percent_fbo"]).replace(".", ",", 1))
            values.append(str(row["commissions"]["sales_percent_fbs"]).replace(".", ",", 1))

            values.append(str(row["marketing_actions"]["current_period_from"]).replace(".", ",", 1))
            values.append(str(row["marketing_actions"]["current_period_to"]).replace(".", ",", 1))
            values.append(str(row["marketing_actions"]["ozon_actions_exist"]).replace(".", ",", 1))

            values.append(str(row["offer_id"]).replace(".", ",", 1))

            values.append(str(row["price"]["auto_action_enabled"]).replace(".", ",", 1))
            values.append(str(row["price"]["currency_code"]).replace(".", ",", 1))
            values.append(str(row["price"]["marketing_price"]).replace(".", ",", 1))
            values.append(str(row["price"]["marketing_seller_price"]).replace(".", ",", 1))
            values.append(str(row["price"]["min_price"]).replace(".", ",", 1))
            values.append(str(row["price"]["old_price"]).replace(".", ",", 1))
            values.append(str(row["price"]["price"]).replace(".", ",", 1))
            values.append(str(row["price"]["retail_price"]).replace(".", ",", 1))
            values.append(str(row["price"]["vat"]).replace(".", ",", 1))

            values.append(str(row["price_indexes"]["color_index"]).replace(".", ",", 1))
            if row["price_indexes"]["external_index_data"] is None:
                values.extend([None, None, None])
            else:
                values.append(str(row["price_indexes"]["external_index_data"]["min_price"]).replace(".", ",", 1))
                values.append(
                    str(row["price_indexes"]["external_index_data"]["min_price_currency"]).replace(".", ",", 1))
                values.append(
                    str(row["price_indexes"]["external_index_data"]["price_index_value"]).replace(".", ",", 1))

            if row["price_indexes"]["ozon_index_data"] is None:
                values.extend([None, None, None])
            else:
                values.append(str(row["price_indexes"]["ozon_index_data"]["min_price"]).replace(".", ",", 1))
                values.append(str(row["price_indexes"]["ozon_index_data"]["min_price_currency"]).replace(".", ",", 1))
                values.append(str(row["price_indexes"]["ozon_index_data"]["price_index_value"]).replace(".", ",", 1))

            if row["price_indexes"]["self_marketplaces_index_data"] is None:
                values.extend([None, None, None])
            else:
                values.append(
                    str(row["price_indexes"]["self_marketplaces_index_data"]["min_price"]).replace(".", ",", 1))
                values.append(
                    str(row["price_indexes"]["self_marketplaces_index_data"]["min_price_currency"]).replace(".", ",",1))
                values.append(
                    str(row["price_indexes"]["self_marketplaces_index_data"]["price_index_value"]).replace(".", ",", 1))

            values.append(str(row["product_id"]).replace(".", ",", 1))
            values.append(str(row["volume_weight"]).replace(".", ",", 1))

            # values.append(str(row["acquiring"]))
            # values.append(str(row["product_id"]))
            # values.append(str(row["offer_id"]))
            # values.append(str(row["price"]["currency_code"]))
            # values.append(str(row["price"]["price"]).replace(".", ",", 1))
            # values.append(str(row["price"]["old_price"]).replace(".", ",", 1))
            # values.append(str(row["price"]["retail_price"]).replace(".", ",", 1))
            # values.append(str(row["price"]["vat"]).replace(".", ",", 1))
            # values.append(str(row["price"]["min_price"]))
            # values.append(str(row["price"]["marketing_price"]).replace(".", ",", 1))
            # values.append(str(row["price"]["marketing_seller_price"]).replace(".", ",", 1))
            # values.append(str(row["price"]["auto_action_enabled"]))
            # values.append(str(row["price_indexes"]["external_index_data"]["min_price"]).replace(".", ",", 1))
            # values.append(str(row["price_indexes"]["external_index_data"]["min_price_currency"]))
            # values.append(str(row["price_indexes"]["external_index_data"]["price_index_value"]).replace(".", ",", 1))
            # values.append(str(row["price_indexes"]["ozon_index_data"]["min_price"]).replace(".", ",", 1))
            # values.append(str(row["price_indexes"]["ozon_index_data"]["min_price_currency"]))
            # values.append(str(row["price_indexes"]["ozon_index_data"]["price_index_value"]).replace(".", ",", 1))
            # values.append(str(row["price_index"]).replace(".", ",", 1))
            # values.append(str(row["price_indexes"]["self_marketplaces_index_data"]["min_price"]).replace(".", ",", 1))
            # values.append(str(row["price_indexes"]["self_marketplaces_index_data"]["min_price_currency"]))
            # values.append(str(row["price_indexes"]["self_marketplaces_index_data"]["price_index_value"]).replace(".", ",", 1))
            # values.append(str(row["commissions"]["sales_percent"]))
            # values.append(str(row["commissions"]["sales_percent_fbo"]))
            # values.append(str(row["commissions"]["sales_percent_fbs"]))
            # values.append(str(row["commissions"]["fbo_fulfillment_amount"]))
            # values.append(str(row["commissions"]["fbo_direct_flow_trans_min_amount"]))
            # values.append(str(row["commissions"]["fbo_direct_flow_trans_max_amount"]))
            # values.append(str(row["commissions"]["fbo_deliv_to_customer_amount"]).replace(".", ",", 1))
            # values.append(str(row["commissions"]["fbo_return_flow_amount"]))
            # values.append(str(row["commissions"]["fbo_return_flow_trans_min_amount"]))
            # values.append(str(row["commissions"]["fbo_return_flow_trans_max_amount"]))
            # values.append(str(row["commissions"]["fbs_first_mile_min_amount"]))
            # values.append(str(row["commissions"]["fbs_first_mile_max_amount"]))
            # values.append(str(row["commissions"]["fbs_direct_flow_trans_min_amount"]))
            # values.append(str(row["commissions"]["fbs_direct_flow_trans_max_amount"]))
            # values.append(str(row["commissions"]["fbs_deliv_to_customer_amount"]).replace(".", ",", 1))
            # values.append(str(row["commissions"]["fbs_return_flow_amount"]))
            # values.append(str(row["commissions"]["fbs_return_flow_trans_min_amount"]))
            # values.append(str(row["commissions"]["fbs_return_flow_trans_max_amount"]))
            # values.append(str(row["volume_weight"]).replace(".", ",", 1))
            # используем numpy для быстроты программы
            values = numpy.array([values])
            ans = numpy.concatenate((ans, values), axis=0)
        needed_keys = self.check_keys(keys)
        return ans.tolist(), ans.shape[0], needed_keys

    def products(self, file: str):
        file = file.replace("\ufeff", "").replace("\"", "").replace("\'", "")
        ans = list(map(lambda x: x.split(";"), file.split("\n")))[:-1]
        needed_keys = self.check_keys(ans)
        return ans, len(ans), needed_keys

    def stock_on_warehouses(self, file: list | dict):
        keys = ["sku", "warehouse_name", "item_code", "item_name", "promised_amount", "free_to_sell_amount",
                "reserved_amount", "idc"]
        ans = numpy.array([keys])
        for row in file:
            values = list(row.values())
            # используем numpy для быстроты программы
            values = numpy.array([values])
            ans = numpy.concatenate((ans, values), axis=0)
        needed_keys = self.check_keys(keys)
        return ans.tolist(), ans.shape[0], needed_keys

    def analytics(self, file: list | dict) -> tuple[list, int, list | None]:
        keys = ["sku_id", "sku_name", "day", "revenue", "ordered_units", "hits_view_search", "hits_view_pdp",
                "hits_view", "hits_tocart_search", "hits_tocart_pdp", "hits_tocart", "session_view_search",
                "session_view_pdp", "session_view", "conv_tocart_search", "conv_tocart_pdp", "conv_tocart", "returns",
                "cancellations", "delivered_units", "position_category"]
        ans = numpy.array([keys])
        for row in file:
            values = list()
            dimensions = row["dimensions"]
            # добавляем dimensions
            values.append(dimensions[0]["id"])
            values.append(dimensions[0]["name"])
            values.append(dimensions[1]["id"])
            # добавляем metrics
            values.extend(list(map(lambda x: str(x).replace('.', ','), row["metrics"])))
            # используем numpy для быстроты программы
            values = numpy.array([values])
            ans = numpy.concatenate((ans, values), axis=0)
        # Записываем данные в файл (убирать комментарий при необходимости)
        with open('data/data.json', 'w', encoding='UTF-8') as d:
            # print(json.dumps(json_response, ensure_ascii=False, indent=4))
            json.dump(ans.tolist(), d, ensure_ascii=False, indent=4)
        needed_keys = self.check_keys(keys)
        return ans.tolist(), ans.shape[0], needed_keys

    def sendings(self, file: list[dict], who_is: str) -> tuple[dict, int, list]:
        ans = {
            "main": list(),
            "keys": list(),
            "products": list(),
            "products_keys": list(),
            "financial_products": list(),
            "financial_products_keys": list()
        }
        for key in file[0]:
            match key:
                case "products":
                    ans["products_keys"].extend(list(file[0]["products"][0].keys()))

                case "financial_data":
                    ans["financial_products_keys"].extend(list(file[0]["financial_data"]["products"][0].keys()))
                    ans["financial_products_keys"].pop(ans["financial_products_keys"].index("item_services"))

                    ans["keys"].append("cluster_from")
                    ans["keys"].append("cluster_to")

                    # ans["financial_products_keys"][0].extend(list(
                    #     file[0]["financial_data"]["products"][0]["item_services"].keys()
                    # ))

                case "additional_data":
                    pass

                # case "analytics_data":
                #     ans["keys"].extend(list(
                #         file[0]["analytics_data"].keys()
                #     ))
                case _:
                    ans["keys"].append(key)

        for value in file:
            ans["main"].append(list())

            for key in value.keys():
                match key:
                    case "products":
                        for product in value[key]:
                            data = self.get_items_from_dict(product, "product")
                            # print(data[1])
                            ans["products"].append(data[1])
                            continue
                    case "financial_data":
                        product: int | str | list | dict | None = None
                        for product in value[key]["products"]:
                            data = self.get_items_from_dict(product, "financial")
                            ans["financial_products"].append(data[1])
                            continue

                        if len(value[key]["cluster_from"]) == 0 or len(value[key]["cluster_to"]) == 0:
                            data = RequestOzon.get_additional_sendings(who_is, value["posting_number"])
                            ans["main"][-1].append(data[0])
                            ans["main"][-1].append(data[1])
                        else:
                            ans["main"][-1].append(value[key]["cluster_from"])
                            ans["main"][-1].append(value[key]["cluster_to"])
                    # case "analytics_data":
                    #     data = self.get_items_from_dict(value["analytics_data"])
                    #     ans["main"][-1].extend(data[1])
                    #     continue
                    case "additional_data":
                        # print(value[key])
                        pass
                    case _:
                        ans["main"][-1].append(value[key])
                        continue

        return ans, 0, list()

    def stocks_fbs(self, file: list[dict[str, str | int | list[dict[str, str | int]]]]):
        result: list[list] = list()
        keys = [
            "offer_id",
            "product_id",
            "Сейчас на складе",
            "Зарезервировано",
            "Тип упаковки",
            "sku",
            "Тип склада"
        ]
        result.append(keys)
        for product in file:
            for stock in product["stocks"]:
                result.append([
                    product["offer_id"],
                    product["product_id"],
                    stock["present"],
                    stock["reserved"],
                    stock["shipment_type"],
                    stock["sku"],
                    stock["type"]
                ])

        needed_keys = self.check_keys(keys)

        return result, len(result), needed_keys

    @staticmethod
    def get_items_from_dict(file: dict, plus_key: str = "") -> tuple[list, list]:
        """
        Конвевртирует огромные json из кучи вложенных словарей и списков в красивый список
        :return: tuple(keys, values)
        """
        #  tuple(keys, values)
        keys = list()
        values = list()
        for key, value in file.items():
            keys.append(f"{plus_key}_{key}")

            if key == "actions" or key == "digital_codes":
                if value == list():
                    values.append("")
                else:
                    values.append(";".join(value))
            elif type(value) is dict:
                continue
            else:
                values.append(value)

        return keys, values

    @staticmethod
    def check_keys(keys: list) -> list | None:
        need_to_check = ["sku_id", "sku", "FBO OZON SKU ID", "FBS OZON SKU ID", "Ozon Product ID", ]
        needed_keys = list()
        for i in need_to_check:
            if i in keys:
                n = keys.index(i)
                needed_keys.append(n)
        return needed_keys
        # if 'nmId' in keys:
        #     n = keys.index('nmId')
        #     needed_keys.append(n)
        #     return needed_keys
        # else:
        #     return

    @staticmethod
    def download(file: list | dict, name: str) -> str:
        match name:
            case 'statements':
                with open('data/Финансовые отчёты.json', 'w') as d:
                    # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                    json.dump(file, d, ensure_ascii=False, indent=4)
            case 'statements_old':
                with open('data/Финансовые отчёты.json', 'w') as d:
                    # print(json.dumps(json_response, ensure_ascii=False, indent=4))
                    json.dump(file, d, ensure_ascii=False, indent=4)
        return 'download'

    @staticmethod
    def beta_start(file: list) -> tuple[list, int]:
        if type(file) is type(None):
            sys.exit('file = None')
        ans = list()
        ans.append([])
        for key in file[0].keys():
            ans[0].append(key)
        # print(json.dumps(file, ensure_ascii=False, indent=4))
        for i, row in enumerate(file):
            ans.append([])
            for key, value in row.items():
                ans[i + 1].append(value)
        return ans, len(ans)
