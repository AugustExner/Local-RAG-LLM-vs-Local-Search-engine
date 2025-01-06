import scrapy

class FandomSpider(scrapy.Spider):
    name = "fandom_all1"
    allowed_domains = ["selenagomez.fandom.com"]
    start_urls = ["https://selenagomez.fandom.com/wiki/Selena_Gomez"]

    visited_urls = set()  # Track visited URLs to avoid duplicates

    def parse(self, response):
        # Mark the URL as visited
        self.visited_urls.add(response.url)

        # Extract data on the page (if needed, like the start page)
        yield from self.parse_article(response)

        # Extract and follow all links on the page
        for link in response.css("a::attr(href)").getall():
            full_link = response.urljoin(link)

            # Only follow unvisited internal wiki links within the allowed domain
            if self.allowed_domains[0] in full_link and "/wiki/" in full_link:
                if full_link not in self.visited_urls:
                    self.visited_urls.add(full_link)
                    yield scrapy.Request(url=full_link, callback=self.parse)

    def parse_article(self, response):
        # Extract the title and content of the article
        title = response.css("h1.page-header__title::text").get()
        paragraphs = response.css("div.mw-parser-output > p::text").getall()
        content = "\n".join(paragraphs)

        # Yield the extracted data
        yield {
            "title": title,
            "content": content,
            "url": response.url
        }
