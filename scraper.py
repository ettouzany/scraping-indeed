from bs4 import BeautifulSoup
import requests
from ah import get_url_data
import typing

city: str = 'Casablanca'
job = 'decathlon'
url = f'https://ma.indeed.com/jobs?q={job}&l={city}'

res = requests.get(url)
soup = BeautifulSoup(res.content, 'html5lib')

with open('file.html', 'w') as f:
    f.write(soup.prettify())

with open('file.html', 'r') as f:
    data  =f.readlines()
ids = []
smiha = len('fae6614b8573f18f')
keyword = 'jobKeysWithInfo'
n = len(keyword)
for line in data:
    if(keyword in line and 'true' in line):
        ids.append(line[n + 1:])
ids = [id[: id.index(']')] for id in ids]
ids = ['job_' + id[1:-1] for id in ids if len(id)>3]
hrefs = []
for id in ids:
    hrefs.append(soup.find('a', attrs={'id':id})['href'])
hrefs = list(set(hrefs))
for hr in hrefs:
    print(get_url_data(hr).prettify(),'\n\n\n\n\n\n\n\n\n')



# print(get_url_data('/rc/clk?jk=d425219359845b1a&fccid=1ddeb792915385d4&vjs=3').prettify())

# print(hrefs)
# print(soup.prettify())