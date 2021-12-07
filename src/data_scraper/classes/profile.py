# Default
import sys

sys.path.append("src")

# Third Party
import scrapy
from scrapy.crawler import CrawlerProcess

# Local
from utils.profile import generate_politician_ids, generate_politician_url


class Profile(scrapy.Spider):
    name = "profile"

    def start_requests(self):
        urls = generate_politician_url()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        # Select social media div
        id_link = (
            response.css("div.api-link.ajax-button-wrapper")
            .css("a::attr(href)")
            .getall()
        )

        weblink_list = (
            response.css("ul.arrow-list.arrow-list--links.arrow-list--two-column")
            .css("li")
            .css("a::attr(href)")
            .getall()
        )

        yield {"id": id_link, "weblink": weblink_list}


process = process = CrawlerProcess(
    settings={
        "FEEDS": {
            "src/json/profile.json": {"format": "json"},
        },
    }
)

if __name__ == "__main__":
    process.crawl(Profile)
    process.start()
