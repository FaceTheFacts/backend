import json
from abc import ABC

import scrapy


def populate_urls(data) -> list:
    urls = []
    for item in data:
        urls.append("https://www.landtag-saar.de" + item["url"])

    return urls


class SaarlandHomepageSpider(scrapy.Spider, ABC):
    name = "saarland-politician-sidejob_categories"

    file = open("./src/json/saarland_homepage_data.json")
    json_data = json.load(file)
    start_urls = populate_urls(json_data)

    def _parse(self, response, **kwargs):
        yield {
            "name": response.css("h4.ProfileName::text").get(),
            "sidejob_categories": str(
                response.css("div.table-wrapper")[-1]
                .css("table.table-simple")
                .css("p")
                .css("strong::text")
                .getall()
            ),
        }
