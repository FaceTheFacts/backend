import scrapy
from scrapy import Item, Field


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
            "https://www.bundestag.de/parlament/praesidium/parteienfinanzierung/fundstellen50000/2022/2022-inhalt-879480",
            "https://www.bundestag.de/parlament/praesidium/parteienfinanzierung/fundstellen50000/2021/2021-inhalt-816896",
            "https://www.bundestag.de/parlament/praesidium/parteienfinanzierung/fundstellen50000/2020/2020-inhalt-678704",
            "https://www.bundestag.de/parlament/praesidium/parteienfinanzierung/fundstellen50000/2019/2019-inhalt-588588",
            "https://www.bundestag.de/parlament/praesidium/parteienfinanzierung/fundstellen50000/2018/2018-inhalt-536742",
            "https://www.bundestag.de/parlament/praesidium/parteienfinanzierung/fundstellen50000/2017/2017-inhalt-488236",
            "https://www.bundestag.de/parlament/praesidium/parteienfinanzierung/fundstellen50000/2016/2016-inhalt-401024",
            "https://www.bundestag.de/parlament/praesidium/parteienfinanzierung/fundstellen50000/2015/2015_inhalt-374930",
            "https://www.bundestag.de/parlament/praesidium/parteienfinanzierung/fundstellen50000/2014/2014-216078",
            "https://www.bundestag.de/parlament/praesidium/parteienfinanzierung/fundstellen50000/2013/2013-210652",
            "https://www.bundestag.de/parlament/praesidium/parteienfinanzierung/fundstellen50000/2012/2012-207934",
            "https://www.bundestag.de/parlament/praesidium/parteienfinanzierung/fundstellen50000/2011/2011-204292",
            "https://www.bundestag.de/parlament/praesidium/parteienfinanzierung/fundstellen50000/2010/2010-200876",
            "https://www.bundestag.de/parlament/praesidium/parteienfinanzierung/fundstellen50000/2009/2009-200874",
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
            "#main > div.bt-module-row.bt-pages-overlay > div > div > article > div > div > table > tbody > tr"
        ):
            party = row.css("td:nth-child(1) ::text").get()
            amount = row.css("td:nth-child(2) ::text").get()
            donar = row.css("td:nth-child(3) ::text").getall()
            date = row.css("td:nth-child(4) ::text").get()

            yield PartyDonation(
                party=party,
                amount=amount,
                donar=donar,
                date=date,
            )
