from bs4 import BeautifulSoup
import re


def clean_page(page):
    soup = BeautifulSoup(page, 'lxml')
    body = soup.find('body')

    for element in body.find_all('style'):
        try:
            element.decompose()
        except AttributeError:
            pass

    for element in body.find_all('script'):
        try:
            element.decompose()
        except AttributeError:
            pass

    for header in body.find_all(['header']):
        links = header.find_all('a')
        if len(links) > 15:
            try:
                header.decompose()
            except AttributeError:
                pass

    for element in body.find_all('nav'):
        try:
            element.decompose()
        except AttributeError:
            pass

    for element in body.find_all('footer'):
        try:
            element.decompose()
        except AttributeError:
            pass

    text = re.sub(r'\n+', " ", body.text)

    return text
