import scrapy


class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["www.persoenlich.com"]
    start_urls = ["https://www.persoenlich.com/marktplatz?page=1"]

    def parse(self, response):
        for link in response.xpath("//h2[@class='company']/a"):
            urls = link.xpath("@href").get()
            ab_url = response.urljoin(urls)
            yield response.follow(url=ab_url, callback=self.data_parser)
            
        for page in range(1,21):
            nxt = response.xpath("//span[@class='next']/a/@href").get()
            nxt_page = response.urljoin(nxt)
            yield response.follow(url=nxt_page,callback=self.parse)
            
    def data_parser(self, response):
        yield{
            "Agency Name": response.xpath("(//div[@class='companynamebold']/text())[2]").get(),
            "Address": response.xpath("(//a[@rel='noopener']/text())[4]").get(),
            "Phone": response.xpath("(//p[@class='mb0']/text())[7]").get(),
            "Mail": response.xpath("(//*[@id='stickyheight']/div[2]/div[2]/div[1]/div/p[2]/text())[2]").get(),
            "Website URL": response.xpath("//*[@id='stickyheight']/div[2]/div[2]/div[1]/div/p[3]/a/@href").get()
        }
