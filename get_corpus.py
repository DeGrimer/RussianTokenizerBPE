from concurrent.futures import ThreadPoolExecutor
import requests
from lxml import html
import re
def get_pages_title(continue_params=None):
    url = "https://neolurk.org/w/api.php"
    params = {
    "action": "query",
    "format": "json",
    "list": "allpages",
    "aplimit": 100
    }
    if continue_params:
        params['apcontinue'] = continue_params
    data = requests.get(url=url,params=params).json()
    page_titles = [page['title'] for page in data['query']['allpages']]
    continue_params = data['continue']['apcontinue']
    return page_titles, continue_params
def fetch_content(page):
    url = "https://neolurk.org/w/api.php"
    params = {
        "action": "parse",
        "page": page,
        "format": "json",
    }
    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        data = response.json()
        raw_text = data.get('parse', {}).get('text', {}).get('*', '')
        document = html.document_fromstring(raw_text)
        p = document.xpath('//p')
        return ''.join(par.text_content() for par in p)
    return ''
def get_content(list_titles):
    corpus = ''
    with ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(fetch_content, list_titles), total=len(list_titles), desc="Processing"))
    corpus = ''.join(results)
    return corpus
all_titles = []
continue_params = ''
for i in tqdm(range(100), desc="Processing"):
    page_titles, continue_params = get_pages_title(continue_params)
    all_titles.extend(page_titles)
corpus = get_content(all_titles).replace('Перенаправление на: <|endoftext|>','')
corpus = re.sub('\[[^\[\]]*\]','',corpus)
with open('E:\\lurk\\output.txt', 'w', encoding="utf-8") as f:
    f.write(corpus)