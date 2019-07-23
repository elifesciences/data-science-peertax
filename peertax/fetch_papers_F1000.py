import pathlib
import re
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm_notebook as tqdm

# URLs fetching
urls = []
idx = [1, 4, 5, 6]
with open("../published-xml-urls.html", "r") as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    for i, link in enumerate(soup.find_all('a')):
        xml_file = link.get('href')
        urls.append(xml_file)

# Downloading papers
out_folder = '../data/articles/f1000_articles/'
pathlib.Path(out_folder).mkdir(exist_ok=True)
for url in tqdm(urls):
    r = requests.get(url)
    name = '-'.join([re.split(r'\W+', url)[_] for _ in idx])+'.xml'
    open(out_folder+name, 'wb').write(r.content)
