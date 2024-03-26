import requests
from bs4 import BeautifulSoup

def scrape_car_links(typ, znacka, search, min_price, max_price):
    base_url = f"https://{typ}.bazos.sk"
    page = 0
    car_links = []
    while True:
        page+=20
        url = f"{base_url}/{znacka}/{page}/?hledat={search}&rubriky={typ}&hlokalita=&humkreis=25&cenaod={min_price}&cenado={max_price}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        listings = soup.find_all('h2', class_='nadpis')
        if not listings:
            break
        
        for listing in listings:
            car_link = listing.find('a', href=True)['href']
            car_links.append(base_url + car_link)
    
    return car_links

def check_for_words_in_listing(link, search_words):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    popis = soup.find_all('div', class_='popisdetail')  # Extract text content and convert to lowercase for case-insensitive search
    popis_texts = [tag.get_text(strip=True, separator=' ') for tag in popis]  # Extract text from tags

    # print(popis_text)
    for popis_text in popis_texts:
        for word in search_words:
            if word.lower() in popis_text.lower():
                return True
    
    return False


if __name__ == "__main__":
    typ = 'auto'
    znacka = 'toyota'
    search = ''
    min_price = "1000"
    max_price = '3000'

    
    car_links = scrape_car_links(typ, znacka, search, min_price, max_price)
    print("Scraped car links:")
    for link in car_links:
        if check_for_words_in_listing(link, ['klimatizácia']):
            print(link)
