from urllib.request import Request, urlopen
import urllib
import string
from datetime import datetime
import json
import pymysql


start_url = "https://advcharts.investing.com/advinion2016/advanced-charts/1/1/8/GetRecentHistory?strSymbol=8862&iTop=1500&strPriceType=bid&strFieldsMode=allFields&strExtraData=lang_ID=1&strTimeFrame=1D"


# class GoldPrice:
#     def __init__(self, start_url):
#         self.url = start_url

def priceData(link):
    src = urllib.request.urlopen(link)
    body = src.read().decode("utf-8")
    data = json.loads(body)
    try:
        dataLs = data["data"]
        for item in dataLs:
            storage(item)
    except KeyError:
        print("Wrong Key!!!")

def storage(item):
        conn = pymysql.connect(host="localhost", user="root", passwd="password", db="mysql")
        cur = conn.cursor()
        try:
            cur.execute("USE MINING")
            sql_query = "INSERT INTO GoldData (GoldDate, OpenPrice, HighPrice, LowPrice, LastPrice, Volume)" \
                        " VALUES (%s,%s,%s,%s,%s,%s)"
            try:
                cur.execute(sql_query,
                            (item["date"], item["open"], item["high"], item["low"], item["close"], item["volume"]))
                cur.connection.commit()
                print("successfully imported")
            except KeyError:
                print("Wrong Key!!!")

        finally:
            cur.close()
            conn.close()

# data = GoldPrice(start_url)
priceData(start_url)