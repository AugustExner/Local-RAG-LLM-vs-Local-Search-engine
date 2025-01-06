import scrapy

class FandomSpider(scrapy.Spider):
    name = "fandom_main"
    allowed_domains = ["harrypotter.fandom.com"]
    start_urls = ["https://harrypotter.fandom.com/wiki/Harry_Potter"]

    def parse(self, response):
        # Extract title
        title = response.css("h1.page-header__title::text").get()

        # Extract all text within <p> tags, including text inside <a> tags and other nested tags
        paragraphs = response.css("div.mw-parser-output > p *::text").getall()
        content = "\n".join(paragraphs)

        yield {
            "title": title,
            "content": content.strip(),
            "url": response.url
        }
