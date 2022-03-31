from bs4 import BeautifulSoup
import requests

def get_url_data(url):
    url = 'https://ma.indeed.com' + url
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html5lib')
    return soup.find('div', attrs={'class':'jobsearch-JobComponent'})



# print(get_url_data('/rc/clk?jk=d425219359845b1a&fccid=1ddeb792915385d4&vjs=3').prettify())
