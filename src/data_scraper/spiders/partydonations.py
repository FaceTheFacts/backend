import scrapy
from scrapy import Item, Field
from scrapy.crawler import CrawlerProcess


class PartyDonation(Item):
    party = Field()
    amount = Field()
    donar = Field()
    city = Field()
    date = Field()


class QuotesSpider(scrapy.Spider):
    name = "partydonations"

    def start_requests(self):
        urls = [
            "https://www.bundestag.de/parlament/praesidium/parteienfinanzierung/fundstellen50000/2023-inhalt-928414",
        ]

        for url in urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                dont_filter=True,
                encoding="utf-8",
            )

    def parse(self, response):
        for row in response.css(
            "#main > div.bt-module-row.bt-pages-overlay > div > article > div.bt-artikel__wrapper.col-lg-12.col-lg-offset-0 > div > div > div.bt-standard-content > div > table > tbody > tr"
        ):
            party = row.css("td:nth-child(1) ::text").get()
            amount = row.css("td:nth-child(2) ::text").get()
            donar = [
                text.replace("\u00a0", "")
                for text in row.css("td:nth-child(3) ::text").getall()
            ]
            date = row.css("td:nth-child(4) ::text").get()

            yield PartyDonation(
                party=party,
                amount=amount,
                donar=donar,
                date=date,
            )


process = process = CrawlerProcess(
    settings={
        "FEEDS": {
            "json/partydonation.json": {"format": "json"},
        },
        "FEED_EXPORT_ENCODING": "utf-8",
    }
)

if __name__ == "__main__":
    process.crawl(QuotesSpider)
    process.start()
