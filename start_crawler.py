from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from threading import Thread
from classifier.profile_classifier import MNBClassifier
import config


def run_crawler(input_module_name, classifier):
    print("Crawler started")

    # when using this class to run the crawler, the reactor should be explicitly run
    runner = CrawlerRunner(get_project_settings())

    d = runner.crawl('university_spider', module_name=input_module_name, classifier=classifier)
    d.addBoth(lambda _: reactor.callFromThread(reactor.stop))

    # twisted reactor can run in any thread, but only one thread at a time
    # we give the argument 'installSignalHandlers=False' to run the reactor in a non-main thread.
    reactor.run(installSignalHandlers=False)
    # this script will block until crawling process is finished.

    print("End of reactor method")


def start_reactor(module_name):
    model_path = config.CLASSIFIER_MODEL_DIR + config.CLASSIFIER_MODEL_NAME
    classifier = MNBClassifier(model_path)
    Thread(target=run_crawler, args=[module_name, classifier]).start()


if __name__ == '__main__':
    start_reactor('Human Computer Interaction')
