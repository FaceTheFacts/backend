import copy

from scrapy.crawler import CrawlerProcess

import json
from abc import ABC

import scrapy

from src.data_scraper.utils.search import search_and_locate_element_in_text


def populate_urls(data) -> list:
    urls = []
    for item in data:
        urls.append("https://www.landtag-saar.de" + item["url"])

    return urls


# removed a list of elements from an array and returns a new array that starts from the first removed element
def remove_elements_from_array__from_first_exception(data, exceptions):
    temp_array = copy.deepcopy(data)
    first_exception_location = None
    deleted_elements = 0

    for index in range(len(data)):
        for exception in exceptions:
            if data[index] == exception:

                if exception is exception[0]:
                    first_exception_location = index

                del temp_array[index - deleted_elements]
                deleted_elements += 1

    data = temp_array
    return data[first_exception_location:]


def sidejob_data_switch(html_data: list[str], response) -> list[str]:
    titles = [
        "Berufliche Tätigkeit vor der Mitgliedschaft im Landtag des Saarlandes",
        "Entgeltliche Tätigkeiten neben dem Mandat",
        "Funktionen in Körperschaften und Anstalten des öffentlichen Rechts",
        "Funktionen in Unternehmen",
        "Funktionen in Vereinen, Verbänden und Stiftungen",
        "Funktionen in Parteiorganisationen",
    ]

    # The website is using table rows instead of direct <p> tags
    if not html_data:
        return (
            response.css("div.table-wrapper")[-1]
            .css("table.table-multi")
            .css("td.value")
            .css("p::text")
            .getall()
        )

    # multiple <p>'s with each sidejob as a separate element
    elif len(html_data) > 1:

        data = (
            response.css("div.table-wrapper")[-1]
            .css("table.table-simple")
            .css("p::text")
            .getall()
        )

        # titles use the <strong> tag
        if search_and_locate_element_in_text(html_data[0], "<strong>")[0]:
            return data

        # titles don't use <strong> tags
        else:
            return remove_elements_from_array__from_first_exception(data, titles)

    # single <p> ...
    elif len(html_data) == 1:

        # ... multiple sidejobs stored in <span>, titles stored in <strong>
        if search_and_locate_element_in_text(html_data[0], "<span>")[0]:
            return (
                response.css("div.table-wrapper")[-1]
                .css("table.table-simple")
                .css("span::text")
                .getall()
            )

        # ... multiple sidejobs stored without <span>, titles stored in <strong>
        elif search_and_locate_element_in_text(html_data[0], "<strong>")[0]:
            return (
                response.css("div.table-wrapper")[-1]
                .css("table.table-simple")
                .css("p::text")
                .getall()
            )

        # ... sidejobs stored without <span>, titles stored without <strong>
        else:
            data = (
                response.css("div.table-wrapper")[-1]
                .css("table.table-simple")
                .css("p::text")
                .getall()
            )

            # title is the first element and the sidejob is the second
            if len(data) == 2:
                return [data[1]]

            # there are multiple titles and multiple sidejobs, stored in a single <p>
            else:
                return remove_elements_from_array__from_first_exception(data, titles)

    return []


class SaarlandHomepageSpider(scrapy.Spider, ABC):
    name = "saarland-politician-sidejobs"

    file = open("json/saarland_homepage_data.json")
    json_data = json.load(file)
    start_urls = populate_urls(json_data)

    def _parse(self, response, **kwargs):
        politician_name = response.css("h4.ProfileName::text").get()

        # Return html response from <p> tag
        html_data = (
            response.css("div.table-wrapper")[-1]
            .css("table.table-simple")
            .css("p")
            .getall()
        )

        sidejob_data = sidejob_data_switch(html_data, response)
        if not sidejob_data:
            sidejob_data = ["UNRECOGNISED STRUCTURE"] + html_data

        yield {"name": politician_name, "sidejob_data": sidejob_data}


process = CrawlerProcess(
    settings={
        "FEEDS": {
            "json/saarland_sidejob_data.json": {"format": "json"},
        }
    }
)

if __name__ == "__main__":
    process.crawl(SaarlandHomepageSpider)
    process.start()
