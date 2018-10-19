# -*- coding: utf-8 -*-
import scrapy


class DoubandianyingSpider(scrapy.Spider):
    name = 'doubandianying'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):

        # item = {}

        li_lists = response.xpath("//div[@class='article']//li")



        for li in li_lists:
            item = {}
            # item = doubanItem()

            item["mv_name"] = li.xpath(".//div[@class = 'info']//a/span[1]/text()").extract_first()

            item["peo_rank"] = li.xpath("./div/div[2]/div[2]/div/span[4]/text()").extract_first()

            item["mv_rank"] = li.xpath("./div/div[2]/div[2]/div/span[2]/text()").extract_first()

            item["mv_author"] = li.xpath("./div/div[2]/div[2]/p[1]/text()").extract_first()

            item["mv_desc"] = li.xpath("./div/div[2]/div[2]/p[2]//span/text()").extract_first()

            item["href"] = li.xpath("./div/div[2]//a/@href").extract_first()

            yield scrapy.Request(item["href"],
                                  callback = self.parse_detail,
                                  meta = {"item": item}
                                  )


        next_url = "https://movie.douban.com/top250"+ response.xpath("//span[@class='next']/a/@href").extract_first()

        print(next_url)

        if next_url is not None:

            yield scrapy.Request(next_url,callback=self.parse)


    def parse_detail(self,response):

        item = response.meta["item"]

        item["content"] = response.xpath("//span[@property='v:summary']/text()").extract()

        # print(item)
        yield item
