import os
from bs4 import BeautifulSoup
import re
from ontology.manage_onto import ITOntologyManager
from preprocessor import clean_page


def check_page(page, module_name):
    onto = ITOntologyManager()
    synonyms = onto.get_synonyms(module_name)
    synonyms.append(module_name)

    count = 0
    page_text = clean_page(page)
    page_lower = page_text.lower()
    for word in synonyms:
        count = count + page.count(word)

    # pattern = re.compile(r'(dr|mr|ms|mrs|prof)\.? ?((ms|mrs)\.?)? ?((\w\.)+)? ?(\w+){1,3}', re.I)

    soup = BeautifulSoup(page.lower(), 'lxml')
    re_interest = soup.find(text='res')

    parent_tag = None

    for i in range(0,5):
        pass

if __name__ == '__main__':
    with open('./classifier/training_data/profiles/ucsc.cmb_profile_kph_.html', 'r') as f:
        page = f.read()
    module_name = "Image_Processing"
    print(check_page(page, module_name.lower()))
