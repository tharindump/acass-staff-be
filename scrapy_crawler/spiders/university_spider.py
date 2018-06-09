from scrapy.spiders import CrawlSpider, Rule
from scrapy_crawler.items import UniversityWebPageItem
from scrapy.linkextractors import LinkExtractor
from managedb import get_db
import score_calc

class UniversitySpider(CrawlSpider):
    name = "university_spider"

    rules = [
        Rule(
            LinkExtractor(
                allow=[],
                deny=[r'\?\w+=\w+'],
                canonicalize=False,
                unique=True
            ),
            follow=True,
            callback="parse_page"
        )
    ]

    def __init__(self, *args, **kwargs):
        super(UniversitySpider, self).__init__()

        db = get_db()
        self.start_urls = []

        # check if the database exists
        if db:
            uni_col = db.get_collection('universities')
            result = uni_col.find({}, {"_id": 0, "name": 0})
            for res in result:
                self.start_urls.append(res['url'])

            # getting allowed domains from start_urls
            self.allowed_domains = []
            # for url in self.start_urls:
            #     self.allowed_domains.append(url.split("//www.")[-1].split("/")[0])
            self.allowed_domains.append(self.start_urls[0].split("//www.")[-1].split("/")[0])

        else:
            raise Exception("Cannot connect to database")

        if 'module_name' in kwargs:
            self.module_name = kwargs.get('module_name')

    def parse_page(self, response):
        item = UniversityWebPageItem()
        item['title'] = self.get_title(response)
        item['url'] = response.url
        relevance_score = score_calc.calculate_relevance_score(response.text, self.module_name)
        item['score'] = relevance_score

        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        # print(response.url, item['title'])

        yield item

    def get_title(self, response):
        return response.selector.xpath('//title/text()').extract_first()
