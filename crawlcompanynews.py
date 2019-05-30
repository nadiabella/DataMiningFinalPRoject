from bs4 import BeautifulSoup
import requests
import pymysql.cursors

def get_url(urls):

    source = requests.get(urls[0]).text
    soup = BeautifulSoup(source, "lxml")
    newslink = soup.find_all("div", {"class": "views-field views-field-title"})
    companylist = urls[1]

    for _ in newslink:
        headline = _.find("a").get_text()
        url = _.find("a").attrs["href"]
        get_data(companylist,headline,url)


def get_data(companylist,headline,url):
    article = ""
    new_url = "https://www.theedgemarkets.com" + url
    print(new_url)
    try:
         source = requests.get(new_url).text
         soup = BeautifulSoup(source, "lxml")
         news = soup.find("div",{"property": "content:encoded"}).find_all("p")
         for _ in news:
             article += _.getText()
         newsdate = soup.find("span", {"class": "post-created"}).getText()
         store(newsdate,companylist, headline,article,new_url)
    except:
        print("you hit an error")


def store(date_news,companylistname,headline,newsarticle,newspage):


    conn = pymysql.connect(host="localhost", user="root", passwd="password", db="mysql")
    cur = conn.cursor()
    try:
        cur.execute("USE crawlnews")
        sql_query = "INSERT INTO banknews (date_news,companylistname,headline,newsarticle,newspage)" \
                    "VALUES (%s,%s,%s,%s,%s)"
        try:
            cur.execute(sql_query,(date_news,companylistname,headline,newsarticle,newspage))

        except ValueError:
                print(""
                      "this is the end of your data")
        cur.connection.commit()

    finally:
        cur.close()
        conn.close()


company_news_urls = []
company_name = ["AXIATA", "TNB", "PETRONAS"]


for item in company_name:
    for i in range (0,5):
        company_news_urls.append(["https://www.theedgemarkets.com/search-results?page={0}&keywords={1}".format(i,item), item])
for item in company_news_urls:
    get_url(item)