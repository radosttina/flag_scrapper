import requests
from bs4 import BeautifulSoup
import os

url = 'https://en.wikipedia.org/wiki/Gallery_of_sovereign_state_flags'
resp = requests.get(url)

soup = BeautifulSoup(resp.text, 'html.parser')

data = {}

os.mkdir('data')

soup.select('li.gallerybox')
for box in soup.select('li.gallerybox'):
    country = box.text.strip().replace('Flag of ', '')
    flag_url = 'http://en.wikipedia.org' + box.find('a').attrs['href']
    data[country] = flag_url

for country, flag_page_url in list((data.items())):
    resp = requests.get(flag_page_url)
    flag_soup = BeautifulSoup(resp.text, 'html.parser')
    image_url = 'https:' + flag_soup.select('div.fullImageLink')[0].find('a').attrs['href']
    image_resp = requests.get(image_url)
    if image_resp.status_code == 200:
        with open("./data/" + country + ".svg", 'wb') as f:
            f.write(image_resp.content)