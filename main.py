# get category
# get detail
# save json

from category import get_breeds
from detail import get_detail

if __name__ == '__main__':
    breeds = get_breeds()
    print(breeds)
    for breed in breeds:
        print(breed.name, breed.url)
        get_detail(breed.url, breed.name)


