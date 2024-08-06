import scrapy
from douban.items import DoubanItem

class DbspiderSpider(scrapy.Spider):
    name = "dbspider"
    allowed_domains = ["douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    def parse(self, response, **kwargs):

        if response.status == 200:
            print("获取响应成功！")
        else:
            print("失败！", + response.status)
            pass

        # 获取所有的电影节点
        node_list = response.xpath('//*[@id="content"]/div/div[1]/ol/li')

        for node in node_list:
            item = DoubanItem()
            item['movie_name'] = node.xpath('./div/div[2]/div[1]/a/span[1]/text()').extract_first()
            item['details'] = node.xpath('./div/div[2]/div[2]/p[1]/text()').extract_first().strip().replace('   ','; ')
            item['stars'] = node.xpath('./div/div[2]/div[2]/div/span[2]/text()').extract_first()
            yield item

        # 模拟翻页
        part_url = response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').extract_first()

        # 判断是否为最后一页
        if part_url != None:
            next_url = response.urljoin(part_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse
            )

        pass
