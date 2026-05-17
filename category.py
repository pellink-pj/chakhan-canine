import requests as rq
from bs4 import BeautifulSoup

from pydantic import BaseModel

class Breed(BaseModel):
    name: str
    url: str

base_url = 'https://www.akc.org/'

def get_breeds():
    response = rq.get(base_url)
    soup = BeautifulSoup(response.text, 'lxml')
    breed_search = soup.find(id='homepage-hero-breed-search')
    breeds = []
    
    for breed in breed_search.find_all('option'):
        breeds.append(Breed(name=breed.text, url=breed['value']))

    return list(filter(lambda x: x.url != '', breeds))


if __name__ == '__main__':
    breeds = get_breeds()
    for breed in breeds:
        print(breed.name, breed.url)