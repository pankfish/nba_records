import scrapy
from scrapy_splash import SplashRequest



class RecordsSpider(scrapy.Spider):
    name = 'records'
    allowed_domains = ['www.nba.com']
    

    script = '''
        function main(splash, args)
            splash:set_user_agent('Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36')
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            splash:set_viewport_full()
            return splash:html()
        end
    '''
    def start_requests(self):
        yield SplashRequest(url="https://www.nba.com/standings", callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })
    def parse(self, response):
        for team in response.xpath("//tbody/tr"):
            position = team.xpath(".//td/div/a/@data-pos").get()
            name = team.xpath(".//td/div/a/@data-text").get()
            conference = team.xpath(".//td/div/a/@data-section").get()
            wins = team.xpath("(.//td)[2]/text()").get()
            losses = team.xpath("(.//td)[3]/text()").get()
            yield{
                'position': position,
                'name': name,
                'conference': conference,
                'wins': wins,
                'losses': losses
            }