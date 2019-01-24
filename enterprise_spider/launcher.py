from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

# from enterprise_spider.spiders.list_spider import ListSpider
# from enterprise_spider.spiders.baidu_spider import BaiduSpider
# from enterprise_spider.spiders.wiki_spider import WikiSpider
from enterprise_spider.spiders.web_spider import WebSpider

settings = get_project_settings()
configure_logging(settings)
runner = CrawlerRunner(settings)
runner.crawl(WebSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run()
