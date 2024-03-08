import requests, wget, os
import xml.etree.ElementTree as ET
from multiprocessing.pool import ThreadPool
links = []
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"

base_url = 'https://www.svgrepo.com/collection/puresugarduotone-line-icons/'
save_path = 'Puresugarduotone Line'
total_pages = 36
os.makedirs('../svgs/' + save_path, exist_ok=True)

for i in range(total_pages+1):
    url = base_url + str(i)
    res = requests.get(url)
    if res.status_code != 200:
        break
    root = ET.fromstring(res.text)
    for node in root.iter():
        for key, value in node.attrib.items():
            if key == 'src' and value.startswith('https://www.svgrepo.com/show/'):
                links.append(value)

def download_file(link):
    filename = wget.filename_from_url(link)
    file = requests.get(link, stream=True, headers={'User-Agent': user_agent})
    open('../svgs/' + save_path + '/' + filename, 'wb').write(file.content)

ThreadPool(20).map(download_file, links)