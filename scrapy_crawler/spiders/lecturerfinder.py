import scrapy
from bs4 import BeautifulSoup
import re

from managedb import get_db
from ontology.manage_onto import ITOntologyManager
from preprocessor import clean_page
from scrapy_crawler.items import LecturerPageItem


class LecturerFindSpider(scrapy.Spider):

    name = "lecturerfinder"
    allowed_domains = ['ucsc.cmb.ac.lk']

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'scrapy_crawler.middlewares.IgnoreURLsDownloaderMiddleWare': None,
        },
        'ITEM_PIPELINES': {
            'scrapy_crawler.pipelines.LecturerFinderPipeline': 300,
            'scrapy_crawler.pipelines.ScrapyCrawlerPipeline': None,
            'scrapy_crawler.pipelines.JsonPipeline': None,
        },
        'LOG_ENABLED': True,
        'LOG_FILE': 'log2_info_.log',
    }

    def __init__(self, *args, **kwargs):
        super(LecturerFindSpider, self).__init__()

        if 'subject_name' in kwargs:
            self.subject_name = kwargs.get('subject_name')
            print(self.subject_name)

            self.database = get_db()
            index_store = self.database.get_collection('index_store')
            urls = index_store.find({'score': 1}, {"_id": 0, "added_date": 0})

            self.onto = ITOntologyManager()

            for url in urls:
                self.start_urls.append(url['url'])

        else:
            raise Exception("Subject Name shoud be supported to continue.")

    def parse(self, response):
        # lecturer links
        soup = BeautifulSoup(response.text, 'lxml')

        print(response.url)

        synonyms = self.onto.get_synonyms(self.subject_name)
        self.subject_name = self.subject_name.replace("_", " ")
        synonyms.append(self.subject_name)

        count = 0
        page_text = clean_page(response.text)
        page_lower = page_text.lower()
        re_in = ['research interest', 'research topics']

        if any(x in page_lower for x in re_in):
            for word in synonyms:
                word = word.lower()
                count = count + page_lower.count(word)

        if count >= 1:
            item = LecturerPageItem()
            item['url'] = response.url
            item['subject'] = self.subject_name
            yield item