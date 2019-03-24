import datetime
import io
from collections import OrderedDict

import rows
import scrapy
from rows.plugins.utils import slug


class FestivalDeCuritibaSpider(scrapy.Spider):
    name = "festival-de-curitiba"
    url = "http://festivaldecuritiba.com.br/atracoes/{page_number}/?date={date}"

    def make_list_request(self, date, page_number):
        return scrapy.Request(
            url=self.url.format(date=date, page_number=page_number),
            meta={"date": date, "page_number": page_number}
        )

    def start_requests(self):
        start_date = datetime.date(2019, 3, 26)
        final_date = datetime.date(2019, 4, 7)
        date = start_date
        one_day = datetime.timedelta(days=1)
        while date <= final_date:
            yield self.make_list_request(date=date, page_number=1)
            date += one_day

    def parse(self, response):
        meta = response.request.meta

        table = rows.import_from_xpath(
            io.BytesIO(response.body),
            rows_xpath='//article[@class="featured-attractions__item"]',
            fields_xpath=OrderedDict([
                ("name", ".//h3//a/text()"),
                ("category", ".//h4//a/text()"),
                ("url", ".//h4//a/@href"),
                ("thumbnail_url", ".//img/@src"),
            ]),
        )
        for row in table:
            data = row._asdict()
            del data["category"]  # Not needed here, will get on next request
            yield scrapy.Request(
                url=data["url"],
                meta={"data": data},
                callback=self.parse_event,
            )

        if response.xpath("//a[text() = 'Próxima >>']"):
            yield self.make_list_request(date=meta["date"], page_number=meta["page_number"] + 1)

    def parse_event(self, response):
        meta = response.request.meta

        data = meta["data"].copy()
        keys = [slug(key) for key in response.xpath("(//ul[@class='details-list'])[1]//li/text()").extract()]
        values = response.xpath("(//ul[@class='details-list'])[1]//li/span/text()").extract()
        data.update(dict(zip(keys, values)))
        ticket = response.xpath("(//a[contains(@href, 'ingresso.festivaldecuritiba.com.br')])[1]/@href").extract()
        data["ticket_url"] = ticket[0] if ticket else None
        image = response.xpath("//div[@class='about-image gallery-content']//img/@src").extract()
        data["image_url"] = image[0] if image else None
        data["schedule"] = "|".join(response.xpath("//div[@class='event-schedules']//p//text()").extract())
        data["description"] = "\n".join(response.xpath("//div[@class='event-description']//p//text()").extract()).replace("\xa0", " ")
        cast = []
        for line in response.xpath("//div[@class='event-datasheet']//p"):
            cast.append(" ".join(line.xpath(".//text()").extract()).replace("  ", " "))
        data["cast"] = "|".join(cast)

        translate_keys = [
            ("evento", "category"),
            ("genero", "genre"),
            ("classificacao", "classification"),
            ("duracao", "duration"),
            ("valor", "value"),
        ]
        for original, new in translate_keys:
            if original in data:
                data[new] = data.pop(original)

        yield data
