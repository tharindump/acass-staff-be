from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from threading import Thread
import config
from scrapy_crawler.spiders.lecturerfinder import LecturerFindSpider
from scrapy.utils.log import configure_logging


def run_crawler(subject_name):
    print("Crawler started")

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    # when using this class to run the crawler, the reactor should be explicitly run
    runner = CrawlerRunner(get_project_settings())

    d = runner.crawl('lecturerfinder', subject_name=subject_name)
    d.addBoth(lambda _: reactor.callFromThread(reactor.stop))

    # twisted reactor can run in any thread, but only one thread at a time
    # we give the argument 'installSignalHandlers=False' to run the reactor in a non-main thread.
    reactor.run(installSignalHandlers=False)
    # this script will block until crawling process is finished.

    print("End of reactor method")


def start_reactor(subject_name):
    Thread(target=run_crawler, args=[subject_name]).start()


if __name__ == "__main__":
    start_reactor("Human_Computer_Interaction")
#
