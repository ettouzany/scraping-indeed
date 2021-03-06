from bs4 import BeautifulSoup
import requests
import json
import numpy as np

def get_metadata(metadata):
    divs = metadata.find_all('div')
    if len(divs) >= 3:
        one = divs[0].get_text()
        two = divs[1].get_text()
        three = divs[2].find('a')
        if (three is not None):
            try:
                three = three['href']
            except:
                three = three.get_text()
        else:
            three = ''
    elif len(divs) == 2:
        one = divs[0].get_text()
        two = divs[1].get_text()
        three = ''
    elif len(divs) == 1:
        one = divs[0].get_text()
        two = ''
        three = ''
    else:
        one = ''
        two = ''
        three = ''
    return one, two, three

def get_description(description):
    description2 = description.find('div')
    if (description2 is not None):
        description = description2
    if (description.get_text() == ''):
        description = description.find_next('div')
    ps = description.find_all('p')
    if (len(ps) == 0):
        ps = description.find_all('div')
    li = description.find_all('li')
    if (ps is not None):
        ps = [p.get_text() for p in ps]
    else:
        ps = []
    if (li is not None):
        li = [l.get_text() for l in li]
    else:
        li = []
    desc1 = '\n'.join(ps + li)
    desc2 = description.get_text()
    desc_html = description.prettify().replace('"', "'").strip()
    return desc1, desc2, desc_html

def get_info_from_div(description, metadata):
    data = {}

    data['poster'] , data['date'] , data['website'] = get_metadata(metadata)
    data['description1'], data['description2'], data['desc_html'] = get_description(description)

    return data


def get_url_data(url):
    url = 'https://ma.indeed.com' + url
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html5lib')
    return soup.find('div', attrs={'class': 'jobsearch-JobComponent'})


def get_jobs(city, job):
    url = f'https://ma.indeed.com/jobs?q={job}&l={city}'
    cards_id = 'mosaic-provider-jobcards'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html5lib')
    soup = soup.find('div', attrs={'id': cards_id})
    links = soup.find_all('a')
    links = list(set([link['href']
                 for link in links if '/rc/clk' in link['href']]))
    return (links)


def main(city, job):
    metadata_class = 'jobsearch-JobMetadataFooter'
    description_id = 'jobDescriptionText'
    
    links = get_jobs(city, job)
    offers = {}
    id = 1
    for link in links:
        div = get_url_data(link)
        with open(f"{city}_{job}_{id}.html", "w") as f:
            f.write(div.prettify())
        metadata = div.find('div', attrs={'class': metadata_class})
        description = div.find('div', attrs={'id': description_id})
        offers[id] = get_info_from_div(description, metadata)
        id += 1
    with open (f'{city}_{job}_offers.json', 'w') as f:
        json.dump(offers, f)


if __name__ == '__main__':
    # main('Casablanca', 'decathlon') 
    m = [[i for i in range(10)] for _ in (range(10))]
    print(np.array(m))