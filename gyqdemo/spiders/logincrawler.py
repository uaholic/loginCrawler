from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scrapy

class LoginSpider(CrawlSpider):
    """Follow categories and extract links."""
    name = 'login'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/',"https://github.com/uaholic/"]

    rules = [
        Rule(LinkExtractor(
            allow=('https://github.com/uaholic/*/$')
        ), callback='parse_directory', follow=True),
    ]

    def start_requests(self):
        yield scrapy.Request("https://github.com/login", callback=self.parse_login)

    def parse_login(self, response):
        # 提取登陆需要的参数
        key = response.xpath("//input[@name='authenticity_token']/@value").extract()[0]
        print("获取验证key",key)
        # 发送请求参数，并调用指定回调函数处理
        yield scrapy.FormRequest.from_response(
            response,
            formdata={  "commit": "Sign in","utf8": "✓","authenticity_token": key,"login": "github账号","password": "github密码"},
            callback=self.after_login
        )
    def after_login(self,response):
        print("登录成功")
        # print(str(response.body,"utf-8"))
        for url in self.start_urls:
            yield self.make_requests_from_url(url)
    def parse_directory(self, response):
        print("scrapyredis根据rule回调")
        print(str(response.body, "utf-8"))