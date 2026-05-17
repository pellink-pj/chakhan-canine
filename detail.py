import requests as rq
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import re # 정규 표현식 사용을 위해 추가
import pprint

# &quot; # "

target_url = "https://www.akc.org/dog-breeds/beagle"

def get_detail(url, breed_name):

    response = rq.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    raw_data_dom = soup.find('div', attrs={'data-js-component': 'breedPage'})
    raw_data = raw_data_dom.get('data-js-props', {})
    json_data = json.loads(raw_data)
    
    # save json
    file_path = f'result/{breed_name}.json'
    
    with open(file_path, 'w') as f:
        json.dump(json_data, f, indent=4)
    return json_data

if __name__ == '__main__':
    get_detail(target_url, 'beagle')