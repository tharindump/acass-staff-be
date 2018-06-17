from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from bs4 import BeautifulSoup
from scrapy_crawler.items import UniversityWebPageItem
from managedb import get_db


class UniversitySpider(CrawlSpider):
    IGNORED_URLS = ['lib', 'library', 'taxonomy', 'img', 'image', 'pdf', 'jpg', 'png', 'repository']

    name = "unispider"
    allowed_domains = ['ucsc.cmb.ac.lk']
    start_urls = ['http://ucsc.cmb.ac.lk/ucsc-staff/academic-staff/', 'http://www.kln.ac.lk']

    rules = (
        Rule(LinkExtractor(unique=True), callback='parse_item', follow=False),
    )
    crawled_urls = set()

    def __init__(self, *args, **kwargs):
        super(UniversitySpider, self).__init__()

        if 'classifier' in kwargs:
            self.classifier = kwargs.get('classifier')
            print(self.classifier.name, '\n')

        self.database = get_db()
        index_store = self.database.get_collection('index_store')
        urls = index_store.find({}, {"_id": 0, "score": 0, "added_date":0})
        for url in urls:
            self.crawled_urls.add(url['url'])

        print("Started " + self.name)

    def parse_item(self, response):
        self.crawled_urls.add(response.url)
        soup = BeautifulSoup(response.body, 'lxml')
        links = self._get_links(response, soup)

        item = UniversityWebPageItem()
        item['url'] = response.url
        if self.classifier:
            score = self.classifier.predict_web_page(response.text)
        else:
            score = 0

        item['score'] = score

        yield item

        for link in links:
            if link not in self.crawled_urls:
                req = Request(link, callback=self.parse_item)
                yield req
            else:
                print("Duplicate Request")

    def _get_links(self, response, soup):
        links = []
        for anchor in soup.find_all('a'):
            href = anchor.get('href')
            if href and not any(x in href for x in self.IGNORED_URLS):
                if href.startswith("/"):
                    href = response.urljoin(href)
                else:
                    continue
                if href not in self.crawled_urls:
                    links.append(href)
        return links
