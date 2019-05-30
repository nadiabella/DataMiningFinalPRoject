from urllib.request import Request, urlopen
import urllib
import string
from datetime import datetime
import json
import pymysql

start_urls = ["https://s3-ap-southeast-1.amazonaws.com/biz.thestar.com.my/json/{}/stocks.js".format(_) for _ in list(string.ascii_uppercase)]


def company(urls):
    for url in urls:
        src = urllib.request.urlopen(url)
        body = str(src.read()).split("=")
        body = body[1].replace("\\r\\n","")
        body = body.replace(body[0:14],"")
        body = body.replace("]};\'","")
        data1 = eval(body)
        for item in data1:
            data(item)


def data(item):
    start_date= "1544212800"
    end_date= "1554312959"
    url = "https://charts.thestar.com.my/datafeed-udf/history?symbol={0}&resolution=D&from={1}&to={2}".format(item["counter"], start_date, end_date)
    src = urllib.request.urlopen(url)
    body = src.read().decode()
    data = eval(body)
    storage(data, item["counter"],item["stockcode"])



def storage(data,company_name, stock_code):
    try:
        data_len = len(data["t"])
        conn = pymysql.connect(host="localhost", user="root", passwd="password", db="mysql")
        cur = conn.cursor()
        try:
            cur.execute("USE Crawler")
            sql_query = "INSERT INTO StockData (StockDate, CompanyName, StockCode, OpenPrice, HighPrice," \
                        " LowPrice, LastPrice, Volume)" \
                        " VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            for i in range(data_len):
                try:
                    cur.execute(sql_query, (datetime.utcfromtimestamp(int(data["t"][i])).strftime("%Y-%m-%d %H:%M:%S"),
                                                company_name, stock_code, data["o"][i], data["h"][i],data["l"][i],
                                                data["c"][i], data["v"][i]))
                except KeyError:
                    continue
                cur.connection.commit()
        finally:
            print("successfully imported")
            cur.close()
            conn.close()
    except KeyError:
        print("Wrong Key!!!")

company(start_urls)