from bs4 import BeautifulSoup
import requests


def get_data(num, page) -> dict:

    """
    When a valid URL is passed in, it opens that page in the Selenium Chromedriver and
    fetches all results in a given range which can be changed
    """

    products = []
    releases = []
    discounts = []
    prices = []

    content = requests.get(page, 'html.parser')
    soup = BeautifulSoup(content.text, features="html.parser")

    for a in soup.findAll('a', attrs = {'class': 'search_result_row'}):
        name = a.find('span', attrs={'class': 'title'})
        price = a.find('div', attrs={'class': 'search_price'})
        discount = a.find('div', attrs={'class': 'search_discount'})
        release = a.find('div', attrs={'class': 'search_released'})

        products.append(name.text.strip())
        releases.append(release.text.strip())

        try:
            prices.append(price.contents[3].strip())
        except IndexError:
            prices.append(price.contents[0].strip())
        
        discounts.append(discount.text.strip())

        if len(prices) == num:
            break

    resultsDict = {'Products':products, 'Prices':prices, 'Releases':releases, 'Discounts':discounts}

    return resultsDict