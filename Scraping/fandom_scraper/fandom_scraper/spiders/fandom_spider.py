import scrapy

class FandomSpider(scrapy.Spider):
    name = "fandom"
    allowed_domains = ["selenagomez.fandom.com"]
    start_urls = ["https://selenagomez.fandom.com/wiki/Selena_Gomez"]

    visited_urls = set()  # Keep track of visited URLs to avoid duplicates

    def parse(self, response):
        # Add the current URL to the visited set
        self.visited_urls.add(response.url)

        # Extract and follow links on the page
        for link in response.css("a::attr(href)").getall():
            full_link = response.urljoin(link)

            # Only follow internal wiki links within the allowed domain and avoid re-processing
            if self.allowed_domains[0] in full_link and "/wiki/" in full_link:
                if full_link not in self.visited_urls:
                    self.visited_urls.add(full_link)
                    yield scrapy.Request(url=full_link, callback=self.parse_article)

    def parse_article(self, response):
        # Extract title, content, and any other relevant information
        title = response.css("h1.page-header__title::text").get()
        paragraphs = response.css("div.mw-parser-output > p::text").getall()
        content = "\n".join(paragraphs)

        yield {
            "title": title,
            "content": content,
            "url": response.url
        }

        # Follow links on this article page to crawl further pages
        for link in response.css("a::attr(href)").getall():
            full_link = response.urljoin(link)

            # Again check to ensure only internal wiki links are followed
            if self.allowed_domains[0] in full_link and "/wiki/" in full_link:
                if full_link not in self.visited_urls:
                    self.visited_urls.add(full_link)
                    yield scrapy.Request(url=full_link, callback=self.parse_article)
