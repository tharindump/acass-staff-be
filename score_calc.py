from preprocessor import clean_page
from ontology.manage_onto import ITOntologyManager
import re


def calculate_relevance_score(page_text, module_name):
    keywords = ["research interest", "research activity", "publication", "award", "academic", "record", "profile"]

    # --Delete <header>, <footer>, <nav>, <script> from the body
    formatted_body = clean_page(page_text)
    bag_of_words = re.split(r" ", formatted_body)
    bag_of_words_count = len(bag_of_words)

    # --to calculate the keywords frequency in a given document
    re_keywords = re.compile('|'.join(keywords), re.I)
    keywords_count = len(re_keywords.findall(formatted_body))

    # --to calculate the frequency of module name and its synonyms
    module_name_formatted = module_name.split(" ")
    re_module_name = re.compile('.'.join(module_name_formatted), re.I)
    module_name_count = len(re_module_name.findall(formatted_body))

    onto = ITOntologyManager()
    synonyms = onto.get_synonyms(module_name)
    re_synonyms = re.compile('|'.join(synonyms), re.I)
    synonyms_count = len(re_synonyms.findall(formatted_body))

    # --calculate relevance score
    keywords_frequency = keywords_count / float(bag_of_words_count)
    synonyms_frequency = synonyms_count / float(bag_of_words_count)
    module_name_frequency = module_name_count / float(bag_of_words_count)

    relevance_score = keywords_frequency + 10 * synonyms_frequency + 50 * module_name_frequency
    return relevance_score
