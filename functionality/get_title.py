import requests
import bs4
def get_title(url):
    r = requests.get(url)
    html = bs4.BeautifulSoup(r.text,'html.parser')
    html = str(html.title)[7:-8]
    message = '.:['+html+']:.'
    return message
